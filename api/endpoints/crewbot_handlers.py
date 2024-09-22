from api.endpoints.base_handler import BaseHandler
import json
from api.controllers.crewbot_controller import CrewBotController

class CrewBotRequestHandler(BaseHandler):
    def initialize(self):
        self.controller = CrewBotController()

    async def post(self, path=None):
        if path == 'chat/init':
            self.initChat()
        
        if path == 'chat':
            self.continueChat()

    async def get(self, *args, **kwargs):
        id_user = self.get_argument("id_user")
        id_chat = self.get_argument("id_chat")
        response = self.controller.loadChat(id_user, id_chat)
        self.handleResponse(response)

    def handleResponse(self, response):
        if response.get("status") == "success":
            self.set_status(200)
        else:
            self.set_status(400)
        self.write(response)

    def initChat(self):
        body = json.loads(self.request.body)
        response = self.controller.initChat(body)
        self.handleResponse(response)

    def continueChat(self):
        body = json.loads(self.request.body)
        response = self.controller.handleChat(body)
        self.handleResponse(response)