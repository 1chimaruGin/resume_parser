import base64
from io import BytesIO
from PIL import Image
from app.api import deps
from app import crud, models, schemas
from app.core.celery_app import celery_app
from typing import Any, List
from sqlalchemy.orm import Session
from pdf2image import convert_from_bytes
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form


router = APIRouter()

def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

@router.get("/", response_model=List[schemas.Application])
async def read_applications(
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
    file: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new application.
    """
    file_content = file.file.read()
    job_description = job_description
    images = []

    if "image" in file.content_type:
        image = Image.open(BytesIO(file_content))
        images.append(image)
    elif "pdf" in file.content_type:
        images = convert_from_bytes(file_content)
    print("We are here ...........")
    encs = [image_to_base64(img) for img in images]
    task = celery_app.send_task(
        "app.worker.process_resume", 
        args=[encs, job_description]
    )
    print("We are still exist ...")
    resume, simi, records = task.get()
    print(f" The task result is: {resume}, {simi}, {records}")
    # is_ready = True
    # name = "John Doe"
    # obj_in = schemas.ApplicationCreate(name=name, resumes=encs, resume_text=resume, job_description=job_description, records=records, is_ready=is_ready)
    # application = crud.application.create_with_owner(
    #     db=db, 
    #     obj_in=obj_in,
    #     owner_id=current_user.id
    # )
    # return application
    

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


@router.post("/test")
def upload(resume: UploadFile = File(...)) -> Any:
    task = celery_app.send_task("app.worker.test_celery", args=[resume.filename])
    print(f"The task result is: {task.get()}")
    return {"msg": "Word received"}
    
