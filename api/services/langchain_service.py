from langchain_openai import ChatOpenAI
from api.services.pinecone_service import PineconeService
from langchain.chains import create_retrieval_chain
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from openai import OpenAI
import traceback
from dotenv import load_dotenv
import os

class LangchainService():
    def __init__(self):
        load_dotenv()
        self.llm = ChatOpenAI(
            model = "gpt-4",
            temperature = 0
        )
        self.pinecone_service = PineconeService()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def createChain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Answer the user's questions based on the context: {context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])

        chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=prompt
        )

        retriever_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an assistant specialized in flight reports. Only retrieve information that answers the user's question, related to flights, technical details, or operational information. Do not return irrelevant data like names unless they are specifically mentioned in the query."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")            
        ])

        history_aware_retriever = create_history_aware_retriever(
            llm = self.llm,
            retriever = self.pinecone_service.getVectorStore().as_retriever(
                search_type="similarity", 
                score_threshold=0.9
            ),
            prompt=retriever_prompt,
        )
        
        return create_retrieval_chain(
            history_aware_retriever,
            chain
        )

    def processChatHistory(self, chat_history):
        new_chat_history = []
        if chat_history: 
            for message in chat_history:
                new_chat_history.append(HumanMessage(content=message["question"]))
                if message["answer"] is not None:
                    new_chat_history.append(AIMessage(content=message["answer"]))
        return new_chat_history
    
    def getAnswer(self, message, chat_history = []):
        chain = self.createChain()
        new_chat_history = self.processChatHistory(chat_history)

        response = chain.invoke({
            "input": message,
            "chat_history": new_chat_history
        })

        if not response.get('context') or len(response.get('context', [])) == 0:
            return {"question": message, "answer": "I did not find any relevant documentation about this subject."}

        return {"question": response.get('input'), "answer": response.get('answer')}
    
    def getRelevantDocuments(self, user_request):
        similar_docs = self.pinecone_service.getVectorStore().similarity_search(user_request, k=100)
        return " ". join([doc.page_content for doc in similar_docs])

    def analyzeReportBasedOnMetric(self, user_request, similar_docs):
        prompt = (
            "You are analyzing flight reports. Answer the user's questions based on the context of flights, delays, and other incidents. "
            "If the user asks about delay causes, destinations, or frequencies, respond specifically in that format. "
            f"User's question: {user_request}"
        )
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": f"{prompt}\n\nReport text: {similar_docs}"}
                ]
            )
            return response.choices[0].message.content.strip()
        except:
            print(traceback.format_exc())
            return ""
        
    def generatePlotlyInstruction(self, user_request, similar_docs):
        prompt = (
            f"Given the following text, generate only Python code using Plotly to create a single graph as per the user's request: '{user_request}'. "
            "Create a separate bar chart for each category mentioned in the text, where each chart shows the frequency of each entity in its respective category. "
            "Here is the text:\n\n"
            f"{similar_docs}\n\n"
            "Return only the necessary Python code for creating the charts using Plotly and nothing else. Avoid adding any text outside of the Python code."
        )
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": f"{prompt}"}
                ]
            )
            plotly_code = response.choices[0].message.content.strip()
            return plotly_code
        except:
            print(traceback.format_exc())
            return ""

    def analyze_graph_image(self, base64_image):
        result = self.llm.invoke(
            [
                SystemMessage(
                    content="You are an expert in data visualization that reads images of graphs and describes the data trends in those images. "
                            "The graphs you will read are line charts that have multiple lines in them. Please pay careful attention to the "
                            "legend color of each line and match them to the line color in the graph. The legend colors must match the line colors "
                            "in the graph correctly."
                ),
                HumanMessage(
                    content=[
                        {"type": "text", "text": "What data insight can we get from this graph?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "auto"
                            },
                        },
                    ]
                )
            ]
        )
        return result.content or "No insights were generated from the image."
