import tornado.web
import json
from bson import ObjectId
import bleach

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "http://localhost:3000")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type, Authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, OPTIONS')

    def options(self, *args, **kwargs):
        self.set_status(200)
        self.finish()

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
            print(response)
        