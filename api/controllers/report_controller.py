import json
from ..services.report_service import ReportService

class ReportController:
    def __init__(self):
        self.service = ReportService()

    def create_report(self, report_dict):
        '''Creates a flight report'''
        return self.service.save_report(report_dict)