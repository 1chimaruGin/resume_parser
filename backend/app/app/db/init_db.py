from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401
from app.models.enums import RoleType

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        # user_in = schemas.UserCreate(
        #     email=settings.FIRST_SUPERUSER,
        #     password=settings.FIRST_SUPERUSER_PASSWORD,
        #     is_superuser=True,
        # )
        user_in = schemas.UserCreate(
            user_name=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            role=RoleType.admin.name,
            organization=None,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
