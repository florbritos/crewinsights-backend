from api.services.token_service import TokenService
from api.controllers.base_controller import BaseController

class TokenController(BaseController):
    def __init__(self):
        super().__init__()
        self.service = TokenService()

    def isValidToken(self, id_user, token):
        data = {
            "id_user" : id_user,
            "token" : token
        }
        errors = self.validation.validate_object_fields(data)
        if bool(errors):
            print(errors)
            return False
        found = self.service.isValidToken(data['id_user'], data['token'])
        print('No match between token and user id' if not found else '')
        return found