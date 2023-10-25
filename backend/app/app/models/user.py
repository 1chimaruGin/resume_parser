from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, Integer, String, Enum, ForeignKey
from app.db.base_class import Base
from app.models.enums import RoleType

if TYPE_CHECKING:
    from .item import Item  # noqa: F401
    from .job import Application  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    role = Column(
        Enum(RoleType),
        nullable=False,
        server_default=RoleType.user.name
    )
    organization = Column(String, index=True, server_default=None)
    items = relationship("Item", back_populates="owner")
    applications = relationship("Application", back_populates="owner")


# class UserGroup(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     org = Column(String, index=True)
#     user_id = Column(Integer, ForeignKey('user.id'))  

