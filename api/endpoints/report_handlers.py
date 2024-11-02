
import json
from api.controllers.report_controller import ReportController
from api.endpoints.base_handler import BaseHandler

class ReportRequestHandler(BaseHandler):
    def initialize(self):
        self.controller = ReportController()

    def post(self):
        body = json.loads(self.request.body)
        sanitized_body = self.sanitize_input(body)
        response = self.controller.save(sanitized_body)
        self.handleResponse(response)