from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.crud.crud_user import user
from app.models.job import Application
from app.schemas.job import ApplicationCreate, ApplicationUpdate


class CRUDApplication(CRUDBase[Application, ApplicationCreate, ApplicationUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: ApplicationCreate, owner_id: int
    ) -> Application:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Application]:
        return (
            db.query(self.model)
            .filter(Application.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_organization(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ):
        organization = user.get_organization(db=db, user_id=owner_id)
        user_ids = user.get_user_ids_by_organization(db=db, organization=organization)
        applications = (
            db.query(self.model)
            .filter(Application.owner_id.in_(user_ids))
            .offset(skip)
            .limit(limit)
            .all()
        )
        return applications


application = CRUDApplication(Application)
