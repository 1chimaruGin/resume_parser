import uuid
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class ApplicationBase(BaseModel):
    name: Optional[str]
    files: Optional[List[str]]
    resume_text: Optional[str]
    job_description: Optional[str]
    records: Optional[Dict[Any, Any]]
    is_ready: bool

class ApplicationCreate(ApplicationBase):
    name: str

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
