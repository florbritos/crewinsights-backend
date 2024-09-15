import re

class Validation:
    def __init__(self):
        self.field_rules = {
            "email": ["required:true", "format:email"],
            "password": ["required:true"]
        }

    def validate_field(self, field, value):
        error = ""
        rules = self.field_rules.get(field, [])
        
        for rule in rules:
            rule_name, rule_value = rule.split(':')
            
            if rule_name == "required" and (value is None or value.strip() == ""):
                error = "This field cannot be empty"
                break
            
            if rule_name == "format" and rule_value == "email":
                regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
                if not re.match(regex, value):
                    error = "Invalid email format"
                    break
        return error

    def validate_object_fields(self, obj):
        list_errors = {}
        
        for field, value in obj.items():
            error = self.validate_field(field, value)
            if error:
                list_errors[field] = error
        
        return list_errors

