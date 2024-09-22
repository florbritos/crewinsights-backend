from api.services.mongodb_service import MongoDB
from api.services.token_service import TokenService
from api.classes.User import User
import bcrypt 

class AccountService:
    def __init__(self):
        self.mongodb_service = MongoDB()
        self.token_service = TokenService()

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
                role=response.get("role")
            )

    def login(self, email, password):  
        user = self.getUserByEmail(email)
        if user:
            hashed_password = user.password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                token = self.token_service.createToken(user)
                self.token_service.saveToken(user.id_user, token)
                user_dict = user.getUserAsDict()
                user_dict.update({"token": token})
                return {"status": "success", "message": "Login successful", "user": user_dict}
            else:
                return {"status": "failed", "message": "Validation failed", "errors": {"password": "Wrong password"}}
        else:
            return {"status": "failed", "message": "Validation failed", "errors": {"email": "Email not found"}}
        
    def logout(self, id_user):
        self.token_service.deleteToken(id_user)
        return {"status": "success", "message": "Logout successful"}