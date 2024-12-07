from api.services.password_recovery_service import PasswordRecoveryService
from api.controllers.base_controller import BaseController

class PasswordRecoveryController(BaseController):
    def __init__(self):
        super().__init__()
        self.service = PasswordRecoveryService()

    def sendOTP(self, data):
        new_data = {
            'email': data.get('email'),
            'otp': data.get('otp')
        }
        errors = self.validation.validate_object_fields(new_data)
        if bool(errors):
            return {"status": "failed", "message": "Validation failed", "errors": errors}
        return self.service.sendOTP(data['email'], data['otp'])
    
    def resetPassword(self, data):
        new_data = {
            'email': data.get('email'),
            'password': data.get('password')
        }
        errors = self.validation.validate_object_fields(new_data)
        if bool(errors):
            return {"status": "failed", "message": "Validation failed", "errors": errors}
        return self.service.resetPassword(data['email'], data['password'])