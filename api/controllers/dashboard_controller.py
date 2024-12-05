import json
from api.services.dashboard_service import DashboardService
from api.controllers.base_controller import BaseController

class DashboardController(BaseController):
    def __init__(self):
        super().__init__()
        self.service = DashboardService()

    def getAllMetricsByUserId(self, id_user):
        try:
            data = {
                'id_user': id_user
            }
            errors = self.validation.validate_object_fields(data)
            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}
            response = self.service.getDashboardByUserId(data['id_user'])
            return {"status": "success", "message": "Dashboard loaded successfully", "result": response}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue while loading the dashboard", "errors": str(e)}
        
    def delete(self, id_user, body):
        try:
            data = {
                'id_user': id_user,
                'id_metric': body.get('id_metric')
            }

            errors = self.validation.validate_object_fields(data)
            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}
            
            self.service.deleteMetricFromDashboard(data['id_user'], data['id_metric'])
            return {"status": "success", "message": "Metric deleted successfully"}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue while deleting a metric", "errors": str(e)}
        
    def add(self, id_user, body):
        try:
            data = {
                'id_user': id_user,
                'id_metric': body.get('id_metric'),
                'metric': body.get('metric')
            }

            errors = self.validation.validate_object_fields(data)
            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}
            
            self.service.addMetricToDashboard(data['id_user'], data['id_metric'], data['metric'])
            return {"status": "success", "message": "Metric added successfully"}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue while adding a new metric", "errors": str(e)}
