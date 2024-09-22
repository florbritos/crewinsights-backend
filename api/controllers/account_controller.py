import json
from api.services.account_service import AccountService
from api.classes.Validation import Validation

class AccountController:
    def __init__(self):
        self.service = AccountService()
        self.validation = Validation()

    def login(self, login_info):
        errors = self.validation.validate_object_fields(login_info)
        if bool(errors):
            return {"status": "failed", "message": "Validation failed", "errors": errors}
        email = login_info.get("email")
        password = login_info.get("password")

        return self.service.login(email, password)
    
    def logout(self, body):
        user_id = body.get("id_user")
        error = self.validation.validate_field("id_user", user_id)
        if error:
            return {"status": "failed", "message": "Validation failed", "errors": error}
        return self.service.logout(user_id)