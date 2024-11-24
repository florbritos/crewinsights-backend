#import tornado.web
from api.endpoints.base_handler import BaseHandler
import json
from api.controllers.searchbot_controller import SearchBotController

class SearchBotRequestHandler(BaseHandler):
    def initialize(self):
        self.controller = SearchBotController()

    async def post(self):
        body = json.loads(self.request.body)
        sanitized_body = self.sanitize_input(body)
        response = self.controller.search(sanitized_body)
        self.handleResponse(response)