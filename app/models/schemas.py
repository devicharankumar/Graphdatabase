from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    person_id: str
    name: str
    email: EmailStr
    role: str
    dept: str = None
    batch: Optional[int] = None

class Job(BaseModel):
    job_id: str
    title: str
    description: str
    posted_by: str
    type: str = "Part-time"
    compensation: Optional[float] = 0.0
