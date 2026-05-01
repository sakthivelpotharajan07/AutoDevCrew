from pydantic import BaseModel

class JobForm(BaseModel):
    title: str
    company: str
    location: str
    position: str
    skills: list[str]
    experience: int
    portfolio: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Software Engineer",
                "company": "ABC Corporation",
                "location": "New York",
                "position": "Full Stack Developer",
                "skills": ["Python", "JavaScript"],
                "experience": 5,
                "portfolio": "https://example.com/portfolio"
            }
        }