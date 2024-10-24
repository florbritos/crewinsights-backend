import re
from bson import ObjectId

class Validation:
    def __init__(self):
        self.field_rules = {
            "email": ["required:true", "format:email", "type:string"],
            "password": ["required:true", "type:string"],
            "id_user": ["required:true", "format:ObjectId"],
            "id_chat": ["required:true", "format:ObjectId"],
            "question": ["required:true", "type:string"],
        }

    def validate_field(self, field, value):
        error = ""
        rules = self.field_rules.get(field, [])
        
        for rule in rules:
            rule_name, rule_value = rule.split(':')
            
            if rule_name == "type":
                if rule_value == "number" and not isinstance(value, (int)):
                    error = "%s must be an integer" % field.capitalize()
                    break
                if rule_value == "string" and not isinstance(value, (str)):
                    error = "%s must be a text" % field.capitalize()
                    break

            if rule_name == "required" and (value is None or str(value).strip() == ""):
                error = "%s cannot be empty" % field.capitalize()
                break
            
            if rule_name == "format":
                regex_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
                if rule_value == "email" and not re.match(regex_email, value):
                    error = "Invalid email format"
                    break
                if rule_value == "ObjectId" and not ObjectId.is_valid(value):
                    error = "%s: Invalid ID format" % field.capitalize()
        return error

    def validate_object_fields(self, obj):
        list_errors = {}
        
        for field, value in obj.items():
            error = self.validate_field(field, value)
            if error:
                list_errors[field] = error
        
        return list_errors

