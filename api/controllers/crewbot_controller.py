import json
from api.services.crewbot_service import CrewBotService
from api.classes.Validation import Validation
from api.services.mongodb_service import MongoDB

class CrewBotController:
    def __init__(self):
        self.service = CrewBotService()
        self.validation = Validation()
        self.mongodb_service = MongoDB()

    def initChat(self, body):
        errors = self.validation.validate_object_fields(body)
        if bool(errors):
            return {"status": "failed", "message": "Validation failed", "errors": errors}
        question = body.get("question")
        id_user = body.get("id_user")
        response = self.service.initChat(id_user, question)
        return {"status": "success", "message": "CrewBot replied successfully", "result": response}
    
    def handleChat(self, body):
        try:
            errors = self.validation.validate_object_fields(body)
            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}
            question = body.get("question")
            id_user = body.get("id_user")
            id_chat = body.get("id_chat")
            response = self.service.handleChat(id_user, id_chat, question)
            return {"status": "success", "message": "CrewBot replied successfully", "result": response}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue with CrewBot", "errors": str(e)}
        
    def loadChat(self, id_user, id_chat):
        try:
            errors = self.validation.validate_object_fields({
                "id_user": id_user,
                "id_chat": id_chat
            })

            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}
            response = self.service.loadChat(id_user, id_chat)
            return {"status": "success", "message": "History Chat loaded successfully", "result": response}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue with CrewBot", "errors": str(e)}