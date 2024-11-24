import json
from ..services.report_service import ReportService
from api.controllers.base_controller import BaseController

class ReportController(BaseController):
    def __init__(self):
        super().__init__()
        self.service = ReportService()

    def save(self, report):
        try:
            new_report = {
                "flight_number": report.get('flight_number'),
                "departure_airport": report.get('departure_airport'),
                "arrival_airport": report.get('arrival_airport'),
                "schedule_departure_time": report.get('schedule_departure_time'),
                "actual_departure_time": report.get('actual_departure_time'),
                "schedule_arrival_time": report.get('schedule_arrival_time'),
                "actual_arrival_time": report.get('actual_arrival_time'),
                "captain_name": report.get('captain_name'),
                "first_officer_name": report.get('first_officer_name'),
                "purser_name": report.get('purser_name'),
                "number_cabin_crew": report.get('number_cabin_crew'),
                "total_number_pax": report.get('total_number_pax'),
                "total_number_infants": report.get('total_number_infants'),
                "total_number_pax_special_assistance": report.get('total_number_pax_special_assistance'),
                "delays": report.get('delays'),
                "reason_delay": report.get('reason_delay'),
                "diverted_emergency_landing": report.get('diverted_emergency_landing'),
                "reason_diverted_emergency_landing": report.get('reason_diverted_emergency_landing'),
                "technical_issues_aircraft": report.get('technical_issues_aircraft'),
                "reason_technical_issues_aircraft": report.get('reason_technical_issues_aircraft'),
                "safety_incident": report.get('safety_incident'),
                "safety_incident_explanation": report.get('safety_incident_explanation'),
                "safety_procedure_not_followed": report.get('safety_procedure_not_followed'),
                "safety_procedure_not_followed_explanation": report.get('safety_procedure_not_followed_explanation'),
                "medical_assistance": report.get('medical_assistance'),
                "medical_assistance_explanation": report.get('medical_assistance_explanation'),
                "unruly_pax": report.get('unruly_pax'),
                "unruly_pax_explanation": report.get('unruly_pax_explanation'),
                "damage_aircraft_equipment": report.get('damage_aircraft_equipment'),
                "damage_aircraft_equipment_explanation": report.get('damage_aircraft_equipment_explanation'),
                "service_not_completed": report.get('service_not_completed'),
                "service_not_completed_explanation": report.get('service_not_completed_explanation'),
                "pax_complaints": report.get('pax_complaints'),
                "pax_complaints_explanation": report.get('pax_complaints_explanation'),
                "additional_comments": report.get('additional_comments')
            }
            errors = self.validation.validate_object_fields(new_report)
            if bool(errors):
                return {"status": "failed", "message": "Validation failed", "errors": errors}
            
            self.service.save(new_report)
            return {"status": "success", "message": "Flight Report submitted successfully"}
        except Exception as e:
            return {"status": "failed", "message": "We encountered an issue while uploading a flight report", "errors": str(e)}