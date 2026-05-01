from pydantic import BaseModel
from typing import Optional

class JobApplicationCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    resume: Optional[str]

class JobApplication(BaseModel):
    job_title: str
    company: str
    location: str
    application_status: Optional[str] = None
    created_date: Optional[str] = None
    id: int = -1

class JobApplicationForm(BaseModel):
    job: JobApplicationCreate
    application: JobApplicationCreate