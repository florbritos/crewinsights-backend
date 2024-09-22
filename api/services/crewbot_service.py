from api.services.langchain_service import LangchainService
from api.services.mongodb_service import MongoDB

class CrewBotService:
    def __init__(self):
        self.langchain_service = LangchainService()
        self.mongodb_service = MongoDB()

    def handleChat(self, id_user, id_chat, message):
        chat_history = self.mongodb_service.getOneDocument('Chats', {"_id": id_chat, "id_user": id_user})
        self.mongodb_service.updateOne('Chats', {"_id": id_chat}, {"$push": {"messages": {"question": message, "answer": None}}})
        return self.handleAnswer(id_user, id_chat, message, chat_history["messages"])

    def initChat(self, id_user, question):
        new_chat = {
            "id_user": id_user,
            "messages": [{"question": question, "answer": None}],
        }

        id_chat = self.mongodb_service.insertOne('Chats', new_chat)
        return self.handleAnswer(id_user, id_chat, question)
    
    def loadChat(self, id_user, id_chat):
        chat_history = self.mongodb_service.getOneDocument('Chats', {"_id": id_chat, "id_user": id_user})
        return chat_history["messages"]

    def handleAnswer(self, id_user, id_chat, question, chat_history=[]):
        response = self.langchain_service.getAnswer(question, chat_history)
        self.mongodb_service.updateOne('Chats', {"_id": id_chat, "id_user": id_user}, {"$set": {"messages.$[msg].answer": response["answer"]}}, array_filters=[{"msg.answer": None}])
        response.update({"id_chat": id_chat})
        return response


