from api.services.crewbot_service import CrewBotService
from api.classes.Validation import Validation

class CrewBotController:
    def __init__(self):
        self.service = CrewBotService()
        self.validation = Validation()

    def initChat(self, body):
        try:
            data = {
                'id_user': body.get('id_user'),
                'question': body.get('question')
            }
            errors = self.validation.validate_object_fields(data)
            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}

            response = self.service.initChat(data['id_user'], data['question'])
            return {"status": "success", "message": "CrewBot replied successfully", "result": response}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue with CrewBot", "errors": str(e)}
    
    def handleChat(self, body):
        try:
            data = {
                'id_user': body.get('id_user'),
                'id_chat': body.get('id_chat'),
                'question': body.get('question')
            }
            errors = self.validation.validate_object_fields(data)
            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}
            
            response = self.service.handleChat(data['id_user'], data['id_chat'], data['question'])
            return {"status": "success", "message": "CrewBot replied successfully", "result": response}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue with CrewBot", "errors": str(e)}
        
    def loadChat(self, id_user, id_chat):
        try:
            data = {
                'id_user': id_user,
                'id_chat': id_chat
            }
            errors = self.validation.validate_object_fields(data)
            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}
            response = self.service.loadChat(data['id_user'], data['id_chat'])
            return {"status": "success", "message": "History Chat loaded successfully", "result": response}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue with CrewBot", "errors": str(e)}
        
    def getAllChatsByUserId(self, id_user):
        try:
            data = {
                'id_user': id_user
            }
            errors = self.validation.validate_object_fields(data)
            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}
            response = self.service.getAllChatsByUserId(data['id_user'])
            return {"status": "success", "message": "History Chats loaded successfully", "result": response}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue with CrewBot", "errors": str(e)}
        
    def deleteChat(self, id_user, id_chat):
        try:
            data = {
                'id_user': id_user,
                'id_chat': id_chat
            }
            errors = self.validation.validate_object_fields(data)
            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}
            self.service.deleteChat(data['id_user'], data['id_chat'])
            return {"status": "success", "message": "History Chat deleted successfully"}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue with CrewBot", "errors": str(e)}