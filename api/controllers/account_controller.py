import json
from api.services.account_service import AccountService
from api.controllers.base_controller import BaseController

class AccountController(BaseController):
    def __init__(self):
        super().__init__()
        self.service = AccountService()

    def login(self, login_info):
        data = {
            'email': login_info.get('email'),
            'password': login_info.get('password')
        }
        errors = self.validation.validate_object_fields(data)
        print(errors)
        if bool(errors):
            return {"status": "failed", "message": "Validation failed", "errors": errors}

        return self.service.login(data['email'], data['password'])
    
    def logout(self, body):
        id_user = body.get("id_user")
        error = self.validation.validate_field("id_user", id_user)
        if error:
            return {"status": "failed", "message": "Validation failed", "errors": error}
        return self.service.logout(id_user)