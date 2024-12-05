class User:
    def __init__(self, id_user, first_name, last_name, dob, address, email, password, nationality, passport, contact_number, role, job_title, avatar):
        self.id_user = id_user
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.address = address
        self.email = email
        self.password = password
        self.nationality = nationality
        self.passport = passport
        self.contact_number = contact_number
        self.role = role
        self.job_title = job_title
        self.avatar = avatar

    def getUserAsDict(self):
        ''' '''
        return {
            "id_user" : self.id_user,
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "dob" : self.dob,
            "address" : self.address,
            "email" : self.email,
            "nationality" : self.nationality,
            "passport" : self.passport,
            "contact_number" : self.contact_number,
            "role" : self.role,
            "job_title" : self.job_title,
            "avatar": self.avatar
        }