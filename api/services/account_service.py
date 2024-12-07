from api.services.mongodb_service import MongoDB
from api.services.token_service import TokenService
from api.services.users_service import UsersService
from api.services.password_service import PasswordService

class AccountService:
    def __init__(self):
        self.mongodb_service = MongoDB()
        self.token_service = TokenService()
        self.users_service = UsersService()

    def login(self, email, password):  
        user = self.users_service.getUserByEmail(email)
        if user:
            hashed_password = user.password
            if PasswordService.isPasswordCorrect(password, hashed_password):
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