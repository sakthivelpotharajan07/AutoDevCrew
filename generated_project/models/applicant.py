class Applicant:
    def __init__(self, name, email, phone_number, cv, cover_letter):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.cv = cv
        self.cover_letter = cover_letter
        self.jobs = []
        self.status = None

    def add_job(self, job):
        self.jobs.append(job)

    def set_status(self, status):
        self.status = status