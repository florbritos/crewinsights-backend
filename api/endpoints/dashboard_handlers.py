#import tornado.web
from api.endpoints.base_handler import BaseHandler
import json
from api.controllers.dashboard_controller import DashboardController

class DashboardRequestHandler(BaseHandler):
    def initialize(self):
        self.controller = DashboardController()

    async def get(self, id_user):
        sanitized_id_user = self.sanitize_input(id_user)
        response = self.controller.getAllMetricsByUserId(sanitized_id_user)
        self.handleResponse(response)