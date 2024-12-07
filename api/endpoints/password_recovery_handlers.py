#import tornado.web
from api.endpoints.base_handler import BaseHandler
import json
from api.controllers.password_recovery_controller import PasswordRecoveryController

class PasswordRecoveryRequestHandler(BaseHandler):
    def initialize(self):
        self.controller = PasswordRecoveryController()

    async def post(self):
        data = json.loads(self.request.body)
        sanitized_data = self.sanitize_input(data)
        response = self.controller.sendOTP(sanitized_data)
        self.handleResponse(response)

    async def patch(self):
        data = json.loads(self.request.body)
        sanitized_data = self.sanitize_input(data)
        response = self.controller.resetPassword(sanitized_data)
        self.handleResponse(response)