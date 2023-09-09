from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, Boolean, JSON, Text

from app.db.base_class import Base

class Application(Base):
    __tablename__ = "job_applications"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, index=True)
    resume = Column(Text)
    job_description = Column(Text)
    records = Column(JSON)
    is_ready = Column(Boolean, default=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
