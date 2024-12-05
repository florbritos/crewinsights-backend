from api.endpoints.base_handler import BaseHandler
import json
from api.controllers.users_controller import UsersController

class UsersRequestHandler(BaseHandler):
    def initialize(self):
        self.controller = UsersController()

    async def get(self):
        response = self.controller.getUsers()
        self.handleResponse(response)

    async def post(self):
        body = json.loads(self.request.body)
        sanitized_body = self.sanitize_input(body)
        response = self.controller.createUser(sanitized_body)
        self.handleResponse(response)

    async def patch(self, id_user):
        body = json.loads(self.request.body)
        sanitized_body = self.sanitize_input(body)
        sanitized_id_user = self.sanitize_input(id_user)
        response = self.controller.updateUser(sanitized_id_user, sanitized_body)
        self.handleResponse(response)

    async def delete(self, id_user):
        sanitized_id_user = self.sanitize_input(id_user)
        response = self.controller.deleteUser(sanitized_id_user)
        self.handleResponse(response)