from api.services.jwt_service import JWTService
from api.services.sql_service import SQLService

class TokenService:
    def __init__(self):
        self.jwt_service = JWTService()
        self.sql_service = SQLService()

    def createToken(self, user):
        return self.jwt_service.createJWTToken(user)
    
    def saveToken(self, id_user, token):
        query = '''INSERT INTO tokens (id_token, fk_id_user, token)
                    VALUES (NULL, %s, %s)'''
        self.sql_service.connect()
        self.sql_service.executeQuery(query, (id_user, token))