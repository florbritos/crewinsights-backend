from api.classes.Validation import Validation

class BaseController(object):
    def __init__(self):
        self.validation = Validation()