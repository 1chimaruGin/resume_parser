from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Application])
def read_applications(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve applications.
    """
    if crud.user.is_superuser(current_user):
        applications = crud.application.get_multi(db, skip=skip, limit=limit)
    else:
        applications = crud.application.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return applications


@router.post("/", response_model=schemas.Application)
def create_application(
    *,
    db: Session = Depends(deps.get_db),
    application_in: schemas.ApplicationCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new application.
    """
    application = crud.application.create_with_owner(db=db, obj_in=application_in, owner_id=current_user.id)
    return application


@router.put("/{id}", response_model=schemas.Application)
def update_application(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    application_in: schemas.ApplicationUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an application.
    """
    application = crud.application.get(db=db, id=id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    if not crud.user.is_superuser(current_user) and (application.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    application = crud.application.update(db=db, db_obj=application, obj_in=application_in)
    return application


@router.get("/{id}", response_model=schemas.Application)
def read_application(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get application by ID.
    """
    application = crud.application.get(db=db, id=id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    if not crud.user.is_superuser(current_user) and (application.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return application


@router.delete("/{id}", response_model=schemas.Application)
def delete_application(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an application.
    """
    application = crud.application.get(db=db, id=id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    if not crud.user.is_superuser(current_user) and (application.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    application = crud.application.remove(db=db, id=id)
    return application
