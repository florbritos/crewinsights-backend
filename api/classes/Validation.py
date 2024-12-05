import re
from bson import ObjectId
from datetime import datetime, timezone

class Validation:
    def __init__(self):
        self.field_rules = {
            'first_name':["required:true", 'type:string'],
            'last_name':["required:true", 'type:string'],
            'dob':["required:true", 'format:date'],
            'address':["required:true", 'type:string'],
            'nationality':["required:true", 'type:string'],
            'passport':["required:true", 'type:string'],
            'contact_number':["required:true", 'type:string'],
            'job_title':["required:true", 'type:string'],
            'avatar':["required:true", 'type:string'],
            'role':["required:true", 'type:string'],
            "token": ["required:true", "format:jwt"],
            "email": ["required:true", "format:email", "type:string"],
            "password": ["required:true", "type:string"],
            "id_user": ["required:true", "format:ObjectId"],
            "id_chat": ["required:true", "format:ObjectId"],
            "id_metric": ["required:true", "format:ObjectId"],
            "question": ["required:true", "type:string"],
            "flight_number": ["required:true"],
            "departure_airport": ["required:true", "format:iata"],
            "arrival_airport": ["required:true", "format:iata"],
            "schedule_departure_time": ["required:true", "format:datetime", "datetime:not_future"],
            "actual_departure_time": ["required:true", "format:datetime", "datetime:not_future"],
            "schedule_arrival_time": ["required:true", "format:datetime", "after:schedule_departure_time", "datetime:not_future"],
            "actual_arrival_time": ["required:true", "format:datetime", "after:actual_departure_time", "datetime:not_future"],
            "captain_name": ["required:true"],
            "first_officer_name": ["required:true"],
            "purser_name": ["required:true"],
            "number_cabin_crew": ["required:true", "format:int", "min:0"],
            "total_number_pax":["required:true", "format:int", "min:0"],
            "total_number_infants": ["required:true", "format:int", "min:0"],
            "total_number_pax_special_assistance":["required:true", "format:int", "min:0"],
            "delays":["format:boolean"],
            "reason_delay":["required:delays"],
            "diverted_emergency_landing":["format:boolean"],
            "reason_diverted_emergency_landing":["required:diverted_emergency_landing"],
            "technical_issues_aircraft":["format:boolean"],
            "reason_technical_issues_aircraft":["required:technical_issues_aircraft"],
            "safety_incident":["format:boolean"],
            "safety_incident_explanation":["required:safety_incident"],
            "safety_procedure_not_followed":["format:boolean"],
            "safety_procedure_not_followed_explanation":["required:safety_procedure_not_followed"],
            "medical_assistance":["format:boolean"],
            "medical_assistance_explanation":["required:medical_assistance"],
            "unruly_pax":["format:boolean"],
            "unruly_pax_explanation":["required:unruly_pax"],
            "damage_aircraft_equipment":["format:boolean"],
            "damage_aircraft_equipment_explanation":["required:damage_aircraft_equipment"],
            "service_not_completed":["format:boolean"],
            "service_not_completed_explanation":["required:service_not_completed"],
            "pax_complaints":["format:boolean"],
            "pax_complaints_explanation":["required:pax_complaints"],
            "additional_comments":[],
        }

    def validate_field(self, field, value, data={}):
        error = ""
        rules = self.field_rules.get(field, [])
        
        for rule in rules:
            rule_name, rule_value = rule.split(':')
            
            if rule_name == "required":
                if rule_value == "true" and (value is None or str(value).strip() == ""):
                    error = "This field cannot be empty"
                    break
                elif rule_value != "true":
                    if data.get(rule_value) and (value is None or str(value).strip() == ""):
                        error = "This field cannot be empty"
                        break

            if rule_name == "format":
                if rule_value == "jwt":
                    regex_jwt = r'^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$'
                    if not re.match(regex_jwt, value):
                        error = "Invalid JWT format"
                        break
                if rule_value == "email":
                    regex_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
                    if not re.match(regex_email, value):
                        error = "Invalid email format"
                        break
                if rule_value == "iata":
                    regex_iata = r'^[A-Z]{3}$'
                    if not re.match(regex_iata, value):
                        error = "IATA code should be 3 letters"
                        break
                if rule_value == "date":
                    regex_date = r'^\d{4}-\d{2}-\d{2}$'
                    if not re.match(regex_date, value):
                        error = "Date format expected YYYY-MM-DD"
                        break
                if rule_value == "time":
                    regex_time = r'^([01]\d|2[0-3]):([0-5]\d)$'
                    if not re.match(regex_time, value):
                        error = "Time format expected HH:MM"
                        break
                if rule_value == "datetime":
                    regex_datetime = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$'
                    if not re.match(regex_datetime, value):
                        error = "Datetime format expected YYYY-MM-DDTHH:MM"
                        break
                if rule_value == "int":
                    try:
                        if not float(value).is_integer():
                            error = "This field must be an integer"
                            break
                    except ValueError:
                        error = "This field must be an integer"
                        break
                if rule_value == "boolean":
                    if not isinstance(value, bool):
                        error = "This field must be true or False"
                        break
                if rule_value == "ObjectId":
                    try:
                        ObjectId(value)
                    except Exception:
                        error = "Invalid ObjectId format"
                        break

            if rule_name == "min":
                try:
                    min_value = float(rule_value)
                    if float(value) < min_value:
                        error = f"The value must be at least {min_value}"
                        break
                except ValueError:
                    error = "Invalid number format"
                    break

            if rule_name == "datetime":
                now = datetime.now(timezone.utc).isoformat()
                if value > now:
                    error = "The date and time cannot be in the future"
                    break

            if rule_name == "after":
                related_field = data.get(rule_value)
                if related_field and datetime.fromisoformat(value) < datetime.fromisoformat(related_field):
                    error = f"This time must be after {rule_value.replace('_', ' ')}"
                    break
        return error

    def validate_object_fields(self, obj):
        list_errors = {}
        for field, value in obj.items():
            error = self.validate_field(field, value, obj)
            
            if error:
                list_errors[field] = error
        
        return list_errors