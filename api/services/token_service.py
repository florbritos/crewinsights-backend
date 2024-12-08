from api.services.jwt_service import JWTService
from api.services.mongodb_service import MongoDB

class TokenService:
    def __init__(self):
        self.jwt_service = JWTService()
        self.mongodb_service = MongoDB()

    def createToken(self, user):
        return self.jwt_service.createJWTToken(user)
    
    def saveToken(self, id_user, token):
        self.mongodb_service.insertOne("Tokens", {"id_user": id_user, "token": token})

    def deleteToken(self, id_user, token):
        self.mongodb_service.deleteOne("Tokens", {"id_user": id_user, "token": token})

    def isValidToken(self, id_user, token):
        return self.mongodb_service.findOne("Tokens", {"id_user": id_user, "token": token})