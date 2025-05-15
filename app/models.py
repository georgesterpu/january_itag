from pydantic import BaseModel
from typing import List

class CandidateProfile(BaseModel):
    full_name: str
    headline: str
    about: str
    skills: List[str]
    github_url: str
    email: str
    phone: str