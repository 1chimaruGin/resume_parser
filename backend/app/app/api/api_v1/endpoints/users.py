from typing import Any, List

from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.api import deps
from app.lib.mailer import send_email
from app.core.config import settings
from app import crud, models, schemas
from app.utils import send_new_account_email

router = APIRouter()


@router.get("", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/register", response_model=schemas.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    register_in: schemas.UserCreate,
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    # if not settings.USERS_OPEN_REGISTRATION:
    # raise HTTPException(
    #     status_code=403,
    #     detail="Open user registration is forbidden on this server",
    # )
    with_name = crud.user.get_by_username(db, user_name=register_in.user_name)
    with_email = crud.user.get_by_email(db, email=register_in.email)
    if with_name or with_email:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    # user_in = schemas.UserCreate()
    user = crud.user.create(db, obj_in=register_in)
    return user


@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    if not crud.user.is_admin(current_user) and current_user.id != user_id:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    user = crud.user.remove(db, id=user_id)
    return user


@router.delete("/me", response_model=schemas.User)
def delete_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete own user.
    """
    user = crud.user.remove(db, id=current_user.id)
    if crud.user.is_admin(current_user):
        raise HTTPException(status_code=400, detail="The admin user cannot be deleted")
    user = crud.user.remove(db, id=current_user.id)
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_admin(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user

@router.post("/contact_us")
def contact_us(
    *,
    contact_in: schemas.Msg,
) -> Any:
    """
    Contact us.
    """
    subject = contact_in.subject
    mail_from = contact_in.email
    mail_to = settings.EMAILS_FROM_EMAIL
    text = contact_in.msg
    try:
        send_email(
            subject=subject,
            recipients=[mail_to],
            body=text,
            sender=mail_from,
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error sending email")
    return status.HTTP_200_OK
