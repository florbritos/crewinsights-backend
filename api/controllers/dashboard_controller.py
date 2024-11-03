import json
from api.services.dashboard_service import DashboardService
from api.classes.Validation import Validation

class DashboardController:
    def __init__(self):
        self.service = DashboardService()
        self.validation = Validation()

    def getAllMetricsByUserId(self, id_user):
        try:
            data = {
                'id_user': id_user
            }
            errors = self.validation.validate_object_fields(data)
            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}
            response = self.service.getAllMetricsByUserId(data['id_user'])
            return {"status": "success", "message": "Dashboard loaded successfully", "result": response}
        except Exception as e:
            return {"status": "failed", "message": "We encountered loading the dashboard", "errors": str(e)}

    
    # def login(self, login_info):
    #     data = {
    #         'email': login_info.get('email'),
    #         'password': login_info.get('password')
    #     }
    #     errors = self.validation.validate_object_fields(data)
    #     if bool(errors):
    #         return {"status": "failed", "message": "Validation failed", "errors": errors}

    #     return self.service.login(data['email'], data['password'])
    
    # def logout(self, body):
    #     id_user = body.get("id_user")
    #     error = self.validation.validate_field("id_user", id_user)
    #     if error:
    #         return {"status": "failed", "message": "Validation failed", "errors": error}
    #     return self.service.logout(id_user)