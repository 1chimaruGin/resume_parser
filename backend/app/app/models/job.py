from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    JSON,
    Text,
    ARRAY,
    Integer,
    Float,
    ForeignKey,
)

from app.db.base_class import Base


class Application(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    resume = Column(ARRAY(String))
    job_description = Column(ARRAY(String))
    score = Column(Float)
    records = Column(JSON)
    is_ready = Column(Boolean, default=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="applications")
