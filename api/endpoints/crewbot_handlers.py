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

    async def get(self, url):
        sanitized_url = self.sanitize_input(url)
        ids = sanitized_url.split('/')[1::2]
        id_user = ids[0]
        id_chat = ids[1] if len(ids) == 2 else None

        if id_user and not id_chat:
            self.getAllChatsByUserId(id_user)
        elif id_user and id_chat:
            self.getChatByChatId(id_user, id_chat)    

    async def delete(self, url):
        sanitized_url = self.sanitize_input(url)
        ids = sanitized_url.split('/')[1::2]
        id_user = ids[0]
        id_chat = ids[1]
        response = self.controller.deleteChat(id_user, id_chat)
        self.handleResponse(response)


    def handleResponse(self, response):
        if response.get("status") == "success":
            self.set_status(200)
        else:
            self.set_status(400)
        self.write(response)

    def initChat(self):
        body = json.loads(self.request.body)
        sanitized_body = self.sanitize_input(body)
        response = self.controller.initChat(sanitized_body)
        self.handleResponse(response)

    def continueChat(self):
        body = json.loads(self.request.body)
        sanitized_body = self.sanitize_input(body)
        response = self.controller.handleChat(sanitized_body)
        self.handleResponse(response)

    def getAllChatsByUserId(self, id_user):
        sanitized_id_user = self.sanitize_input(id_user)
        response = self.controller.getAllChatsByUserId(sanitized_id_user)
        self.handleResponse(response)

    def getChatByChatId(self, id_user, id_chat):
        sanitized_id_user = self.sanitize_input(id_user)
        sanitized_id_chat = self.sanitize_input(id_chat)
        response = self.controller.loadChat(sanitized_id_user, sanitized_id_chat)
        self.handleResponse(response)