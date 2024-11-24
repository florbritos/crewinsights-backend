from api.services.searchbot_service import SearchBotService
from api.controllers.base_controller import BaseController

class SearchBotController(BaseController):
    def __init__(self):
        super().__init__()
        self.service = SearchBotService()

    def search(self, query):
        try:
            data = {
                'question': query
            }
            errors = self.validation.validate_object_fields(data)
            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}
            response = self.service.search(data['question'])
            return {"status": "success", "message": "SearchBot replied successfully", "result": response}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an with SearchBot", "errors": str(e)}
