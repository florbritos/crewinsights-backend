from api.services.mongodb_service import MongoDB
from api.classes.User import User
from api.services.password_service import PasswordService
from api.services.dashboard_service import DashboardService

class UsersService:
    def __init__(self):
        self.mongodb_service = MongoDB()
        self.dashboard_service= DashboardService()

    def getUsers(self):
        users = []
        user_list = self.mongodb_service.getDocuments('Users', {})
        for user in user_list:
            user_class = User(
                    id_user=str(user.get("_id")),
                    first_name=user.get("first_name"),
                    last_name=user.get("last_name"),
                    dob=str(user.get("dob")),
                    address=user.get("address"),
                    email=user.get("email"),
                    password=user.get("password"),
                    nationality=user.get("nationality"),
                    passport=user.get("passport"),
                    contact_number=user.get("contact_number"),
                    job_title=user.get("job_title"),
                    role=user.get("role"),
                    avatar=user.get("avatar")
                )
            users.append(user_class.getUserAsDict())
        return users
    
    def getUserByEmail(self, email):
        response = self.mongodb_service.getOneDocument("Users", {"email": email})
        if response:
            return User(
                id_user=str(response.get("_id")),
                first_name=response.get("first_name"),
                last_name=response.get("last_name"),
                dob=str(response.get("dob")),
                address=response.get("address"),
                email=response.get("email"),
                password=response.get("password"),
                nationality=response.get("nationality"),
                passport=response.get("passport"),
                contact_number=response.get("contact_number"),
                job_title=response.get("job_title"),
                role=response.get("role"),
                avatar=response.get("avatar")
            )
        
    def createUser(self, data):
        email_registered = self.getUserByEmail(data.get('email'))
        if email_registered:
            raise Exception('Email already registered')
        data.update({'password': str(PasswordService.hashPassword(data['password']))})
        id_user = self.mongodb_service.insertOne('Users', data)
        if data.get('role') == 'Admin':
            self.dashboard_service.createDashboard(id_user)
    
    def updateUser(self, id_user, new_data):
        if new_data.get('email'):
            email_registered = self.getUserByEmail(new_data.get('email'))
            if email_registered:
                return {"status": "failed", "message": "Validation failed", "errors": {"email": "Email already registered"}}
        if new_data.get('role') == 'Admin':
            self.dashboard_service.createDashboard(id_user)
        if new_data.get('role') == 'Crew':
            self.dashboard_service.deleteDashboard(id_user)
        self.mongodb_service.updateOne('Users', {"_id": id_user},{"$set": new_data})

    def deleteUser(self, id_user):
        self.dashboard_service.deleteDashboard(id_user)
        self.mongodb_service.deleteOne('Users', {"_id": id_user})
