from langchain_openai import ChatOpenAI
from api.services.pinecone_service import PineconeService
from langchain.chains import create_retrieval_chain
from langchain.schema import HumanMessage, AIMessage
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever

class LangchainService():
    def __init__(self):
        self.llm = ChatOpenAI(
            model = "gpt-4o",
            temperature = 0
        )

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
            retriever = PineconeService().vectorstore.as_retriever(),
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

    def getAnswer(self, message, chat_history):

        chain = self.createChain()
        new_chat_history = self.processChatHistory(chat_history)

        response = chain.invoke({
            "input": message,
            "chat_history": new_chat_history
        })

        return {"question": response.get('input'), "answer": response.get('answer')}





# class LangchainService():
#     def __init__(self):
#         self.llm = ChatOpenAI(
#             model = "gpt-4o",
#             temperature = 0
#         )
#         self.user_memories = None

#     def getUserMemory(self):
#         return self.user_memories
    
#     def setUserMemory(self, id_user, id_chat, chat_history):
#         memory = ConversationBufferMemory(
#                 memory_key=f"memory_{id_user}_{id_chat}",
#                 #memory_key='chat_history',
#                 input_key="question", 
#                 return_messages=True
#             )

#         if chat_history: 
#             for message in chat_history:
#                 memory.chat_memory.messages.append(HumanMessage(content=message["question"]))
#                 if message["answer"] is not None:
#                     memory.chat_memory.messages.append(AIMessage(content=message["answer"]))
#         self.user_memories = memory

#     def getAnswer(self, id_user, message):
#         user_memory = self.getUserMemory()
#         if user_memory is None:
#             raise ValueError("No chat history found for user.")

#         chat_history = user_memory.chat_memory.messages
#         print("messages in memory", user_memory.chat_memory.messages)

#         prompt_template = """
#         Utiliza los mensajes anteriores del chat para ayudar al usuario. Si te piden repetir algo, utiliza el historial del chat para hacerlo. Historial del chat:
#         {chat_history}  
#         """
#         qa = ConversationalRetrievalChain.from_llm(
#             llm=self.llm,
#             retriever=PineconeService().vectorstore.as_retriever(),
#             memory=user_memory,
#             condense_question_prompt=PromptTemplate.from_template(prompt_template),
#         )

#         response = qa({"question": message, "chat_history": chat_history})
#         #user_memory.clear()
#         return {"question": response.get('question'), "answer": response.get('answer')}


# class LangchainService():
#     def __init__(self):
#         self.llm = ChatOpenAI(
#             model = "gpt-4o",
#             temperature = 0
#         )
#         self.user_memories = None

#     def getUserMemory(self):
#         return self.user_memories
    
#     def setUserMemory(self, id_user, id_chat, chat_history):
#         memory = ConversationBufferMemory(
#                 memory_key=f"memory_{id_user}_{id_chat}",
#                 #memory_key='chat_history',
#                 input_key="question", 
#                 return_messages=True
#             )

#         if chat_history: 
#             for message in chat_history:
#                 memory.chat_memory.messages.append(HumanMessage(content=message["question"]))
#                 if message["answer"] is not None:
#                     memory.chat_memory.messages.append(AIMessage(content=message["answer"]))
#         self.user_memories = memory

#     def getAnswer(self, id_user, message):
#         user_memory = self.getUserMemory()
#         if user_memory is None:
#             raise ValueError("No chat history found for user.")

#         chat_history = user_memory.chat_memory.messages
#         print("messages in memory", user_memory.chat_memory.messages)

#         prompt_template = """
#         Utiliza los mensajes anteriores del chat para ayudar al usuario. Si te piden repetir algo, utiliza el historial del chat para hacerlo. Historial del chat:
#         {chat_history}  
#         """
#         qa = ConversationalRetrievalChain.from_llm(
#             llm=self.llm,
#             retriever=PineconeService().vectorstore.as_retriever(),
#             memory=user_memory,
#             condense_question_prompt=PromptTemplate.from_template(prompt_template),
#             verbose=True
#             #question_generator=question_generator_chain,
#         )

#         #response = qa.invoke(message)
#         response = qa({"question": message})
#         return {"question": response.get('question'), "answer": response.get('answer')}
