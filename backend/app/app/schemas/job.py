from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class ApplicationBase(BaseModel):
    name: Optional[str]
    score: Optional[float]
    records: Optional[Dict[Any, Any]]

class ApplicationCreate(ApplicationBase):
    name: str
    resumes: Optional[List[str]]
    job_description: Optional[str]
    resume_text: Optional[str]
    is_ready: bool

class ApplicationUpdate(ApplicationBase):
    pass

class ApplicationInDBBase(ApplicationBase):
    id: int
    name: str

    class Config:
        orm_mode = True

class Application(ApplicationInDBBase):
    pass

class ApplicationInDB(ApplicationInDBBase):
    pass

class JobDescription(BaseModel):
    job_title: Optional[str]
    industry: Optional[str]
    job_description: Optional[str]
