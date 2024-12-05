from api.services.users_service import UsersService
from api.controllers.base_controller import BaseController

class UsersController(BaseController):
    def __init__(self):
        super().__init__()
        self.service = UsersService()

    def getUsers(self):
        try:
            response = self.service.getUsers()
            return {"status": "success", "message": "Users fetched successfully", "result": response}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue while getting the users list", "errors": str(e)}
        
    def createUser(self, body):
        try:
            data = {
                'first_name':body.get("first_name"),
                'last_name':body.get("last_name"),
                'dob':str(body.get("dob")),
                'address':body.get("address"),
                'email':body.get("email"),
                'password':body.get("password"),
                'nationality':body.get("nationality"),
                'passport':body.get("passport"),
                'contact_number':body.get("contact_number"),
                'job_title':body.get("job_title"),
                'role':body.get("role"),
                'avatar': body.get("avatar")
            }

            errors = self.validation.validate_object_fields(data)
            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}
            
            self.service.createUser(data)
            return {"status": "success", "message": "User created successfully"}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue while creating an user", "errors": str(e)}

    def updateUser(self, id_user, body):
        try:
            changes = {
                'first_name':body.get("first_name"),
                'last_name':body.get("last_name"),
                'dob':str(body.get("dob")),
                'address':body.get("address"),
                'email':body.get("email"),
                'password':body.get("password"),
                'nationality':body.get("nationality"),
                'passport':body.get("passport"),
                'contact_number':body.get("contact_number"),
                'job_title':body.get("job_title"),
                'role':body.get("role"),
                'avatar': body.get("avatar")
            }

            #data = {key: value for key, value in changes.items() if value not in [None, ""] and not str(value).isspace()}
            data = {key: value for key, value in changes.items() if key in body}          
            errors = self.validation.validate_object_fields(data)
            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}
            
            response = self.service.updateUser(id_user, data)
            if response:
                return response
            return {"status": "success", "message": "User updated successfully"}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue while updating an user", "errors": str(e)}

    def deleteUser(self, id_user):
        try:
            self.service.deleteUser(id_user)
            return {"status": "success", "message": "User deleted successfully"}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue while deleting an user", "errors": str(e)}