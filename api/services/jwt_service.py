import jwt

class JWTService:
    def createJWTToken(self, user):
        '''It returns a JWT token for authentication'''
        new_user = {
            "user_id": user.id_user,
            "email": user.email,
            "password": user.password
        }
        return jwt.encode(new_user, 'SECRET_KEY', algorithm="HS256")