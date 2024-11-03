from langchain_openai import ChatOpenAI
from api.services.pinecone_service import PineconeService
from langchain.chains import create_retrieval_chain
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever

class LangchainService():
    def __init__(self):
        self.llm = ChatOpenAI(
            model = "gpt-4o",
            temperature = 0
        )
        self.pinecone_service = PineconeService()

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
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            ("human", "Given he above conversation, generate a search query to look up in order to get information relevant to the conversation")
        ])

        history_aware_retriever = create_history_aware_retriever(
            llm = self.llm,
            retriever = self.pinecone_service.getVectorStore().as_retriever(),
            prompt=retriever_prompt
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

        return {"question": response.get('input'), "answer": response.get('answer')}
    
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
