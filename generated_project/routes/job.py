from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class JobRequest(BaseModel):
    name: str
    email: str
    address: str
    phone_number: str
    linkedin: str
    job_title: str
    company: str
    resume: str
    skills: str
    message: str

@app.post("/job")
async def create_job(name: str = Form(...), email: str = Form(...), address: str = Form(...), 
                     phone_number: str = Form(...), linkedin: str = Form(None), 
                     job_title: str = Form(None), company: str = Form(None), 
                     resume: str = Form(None), skills: str = Form(None), message: str = Form(None)):
    return { "name": name, "email": email, "address": address, "phone_number": phone_number, 
             "linkedin": linkedin, "job_title": job_title, "company": company, 
             "resume": resume, "skills": skills, "message": message }