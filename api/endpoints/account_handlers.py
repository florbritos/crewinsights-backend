#import tornado.web
from api.endpoints.base_handler import BaseHandler
import json
from api.controllers.account_controller import AccountController

class AccountRequestHandler(BaseHandler):
    def initialize(self):
        self.controller = AccountController()

    async def post(self):
        ''''''
        login_info = json.loads(self.request.body)
        sanitized_login_info = self.sanitize_input(login_info)
        response = self.controller.login(sanitized_login_info)
        if response.get("status") == "success":
            self.set_status(200)
        else:
            self.set_status(400)
        self.write(response)

    async def delete(self):
        body = json.loads(self.request.body)
        sanitized_body = self.sanitize_input(body)
        response = self.controller.logout(sanitized_body)
        if response.get("status") == "success":
            self.set_status(200)
        else:
            self.set_status(400)
        self.write(response)