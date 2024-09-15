from api.services.sql_service import SQLService
from api.services.token_service import TokenService
from api.classes.User import User
import bcrypt 

class AccountService:
    def __init__(self):
        self.sql_service = SQLService()
        self.token_service = TokenService()

    def getUserByEmail(self, email):
        ''''''
        query = '''SELECT 
                    users.id_user, users.first_name, users.last_name, users.dob, users.address, users.email, users.password, users.nationality, users.passport, users.contact_number, 
                    job_titles.name AS 'job_title', roles.name AS 'role' FROM users
                    INNER JOIN roles ON roles.id_role = users.fk_id_role
                    INNER JOIN job_titles ON job_titles.id_job_title = users.fk_id_job_title
                    WHERE users.email = %s'''
        self.sql_service.connect()
        response = self.sql_service.executeQuery(query, (email))
        if response:
            return User(
            id_user=response[0][0],
            first_name=response[0][1],
            last_name=response[0][2],
            dob=str(response[0][3]),
            address=response[0][4],
            email=response[0][5],
            password=response[0][6],
            nationality=response[0][7],
            passport=response[0][8],
            contact_number=response[0][9],
            job_title=response[0][10],
            role=response[0][11]
        )

    def login(self, email, password):
        ''''''       
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