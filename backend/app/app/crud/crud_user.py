from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from typing import Any, Dict, Optional, Union


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, *, user_name: str) -> Optional[User]:
        user = db.query(User).filter(User.user_name == user_name).first()
        return user

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            user_name=obj_in.user_name,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            role=obj_in.role,
            organization=obj_in.organization,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, user_name: str, password: str
    ) -> Optional[User]:
        user = self.get_by_username(db, user_name=user_name)

        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_admin(self, user: User) -> bool:
        return user.role.name == "admin"

    def is_org(self, user: User) -> bool:
        return user.role.name == "organization"

    def is_user(self, user: User) -> bool:
        return user.role.name == "user"

    def is_guest(self, user: User) -> bool:
        return user.role.name == "guest"

    def what_role(self, user: User) -> str:
        return user.role

    def get_organization(self, db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        return user.organization

    def get_user_ids_by_organization(self, db: Session, organization: str):
        users = db.query(User).filter(User.organization == organization).all()
        user_ids = []
        for user in users:
            user_ids.append(user.id)
        return user_ids


user = CRUDUser(User)
