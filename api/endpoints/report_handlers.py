
import json
from api.controllers.report_controller import ReportController
from api.endpoints.base_handler import BaseHandler

class ReportRequestHandler(BaseHandler):
    def initialize(self):
        self.controller = ReportController()

    def get(self):
        self.write("CrewInsights Server Running")

    def post(self):
        '''Creates a flight report'''
        report_dict = json.loads(self.request.body)
        response = self.controller.create_report(report_dict)
        self.write(response)