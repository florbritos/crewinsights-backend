import tornado.web
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, Content-Type, Authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

    def write(self, chunk):
        if isinstance(chunk, dict):
            chunk = json.dumps(chunk, cls=JSONEncoder)
        super().write(chunk)