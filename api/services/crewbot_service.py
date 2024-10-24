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
            "title": ""
        }

        id_chat = self.mongodb_service.insertOne('Chats', new_chat)
        return self.handleAnswer(id_user, id_chat, question)

    def handleAnswer(self, id_user, id_chat, question, chat_history=[]):
        response = self.langchain_service.getAnswer(question, chat_history)
        self.mongodb_service.updateOne('Chats', {"_id": id_chat, "id_user": id_user}, {"$set": {"messages.$[msg].answer": response["answer"]}}, array_filters=[{"msg.answer": None}])
        response.update({"id_chat": id_chat})
        title = self.getTitle(id_user, id_chat)
        self.mongodb_service.updateOne('Chats', {"_id": id_chat, "id_user": id_user}, {"$set": {"title": title}})
        response.update({"title": title})
        return response
    
    def getTitle(self, id_user, id_chat):
        chat_history = self.mongodb_service.getOneDocument('Chats', {"_id": id_chat, "id_user": id_user})
        question =  "Please choose a title with a maximum of 5 words for our current conversation. Do not base it on the provided context, but only on our actual conversation."
        response = self.langchain_service.getAnswer(question, chat_history["messages"])
        return response['answer']
    
    def loadChat(self, id_user, id_chat):
        chat_history = self.mongodb_service.getOneDocument('Chats', {"_id": id_chat, "id_user": id_user})
        return chat_history
    
    def getAllChatsByUserId(self, id_user):
        chats = self.mongodb_service.getDocuments('Chats', {"id_user": id_user})
        return chats
    
    def deleteChat(self, id_user, id_chat):
        self.mongodb_service.deleteOne('Chats', {"_id": id_chat, "id_user": id_user})


