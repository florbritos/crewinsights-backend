import tornado.web
import json
from bson import ObjectId
import bleach
from api.controllers.token_controller import TokenController
import os

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.token_controller = TokenController()

    def set_default_headers(self):
        allowed_origins = ["https://crewinsights-frontend.vercel.app"]
        origin = self.request.headers.get("Origin")
        if origin in allowed_origins:
            self.set_header("Access-Control-Allow-Origin", origin)
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type, Authorization, CrewInsights-User-ID")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, PATCH, OPTIONS')

    def options(self, *args, **kwargs):
        self.set_status(200)
        self.finish()

    def prepare(self):
        if self.request.method == "OPTIONS" or self.request.uri == "/api/account/session" or self.request.uri == "/api/password-recovery":
            return
        self.validateToken()

    def validateToken(self):
        token = self.request.headers.get("Authorization")
        id_user = self.request.headers.get("CrewInsights-User-ID")
        if not token:
            raise tornado.web.HTTPError(401, reason="Unauthorized: Missing token")
        if not id_user:
            raise tornado.web.HTTPError(401, reason="Unauthorized: Missing user id")
        sanitized_id_user = self.sanitize_input(id_user)
        sanitized_token = self.sanitize_input(token)
        if not self.token_controller.isValidToken(sanitized_id_user, sanitized_token):
            raise tornado.web.HTTPError(401, reason="Unauthorized")

    def write(self, chunk):
        if isinstance(chunk, dict):
            chunk = json.dumps(chunk, cls=JSONEncoder)
        super().write(chunk)

    def sanitize_input(self, data):
        if isinstance(data, dict):
            sanitized_data = {}
            for field, value in data.items():
                if isinstance(value, str):
                    sanitized_data[field] = bleach.clean(value)
                else:
                    sanitized_data[field] = value
            return sanitized_data

        elif isinstance(data, str):
            sanitized_value = bleach.clean(data)
            return sanitized_value
        else:
            raise TypeError("Input must be a dictionary or a string.")
        
    def handleResponse(self, response):
        if response.get("status") == "success":
            self.set_status(200)
            self.write(response)
        else:
            self.set_status(400)
            self.write(response)
            print(response)