from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class ApplicationBase(BaseModel):
    name: Optional[str]
    score: Optional[float]
    records: Optional[Dict[Any, Any]]

class ApplicationCreate(ApplicationBase):
    name: str
    resume: Optional[List[str]]
    job_description: Optional[List[str]]
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

