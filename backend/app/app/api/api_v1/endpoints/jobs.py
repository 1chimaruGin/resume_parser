import os
import re
import base64
import tempfile
import hashlib
from io import BytesIO
from PIL import Image
from app.api import deps
from app import crud, models, schemas
from app.core.celery_app import celery_app
from app.lib.mailer import send_email
from app.lib.download import download_pdf
from typing import Any, List
from sqlalchemy.orm import Session
from pdf2image import convert_from_bytes
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status


router = APIRouter()


def validate_email(email: str):
    pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return pattern.match(email)
    

def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def image_to_pdf(img):
    """
    Save the numpy image as pdf in tempfile
    """
    img = img[:, :, ::-1]
    image = Image.fromarray(img, mode="RGB")
    with tempfile.NamedTemporaryFile(prefix="sample", suffix=".pdf", delete=False) as f:
        f.close()
        image.save(f.name, "PDF", resolution=100.0, save_all=True)
        return f.name


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
    if crud.user.is_admin(current_user):
        applications = crud.application.get_multi(db, skip=skip, limit=limit)
    else:
        applications = crud.application.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return applications


@router.post("/")
async def create_application(
    *,
    files: List[UploadFile],
    jd_file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new application.
    """

    jd_file_content = jd_file.file.read()
    encoded_jd = [
        image_to_base64(content)
        for content in (
            [Image.open(BytesIO(jd_file_content))]
            if "image" in jd_file.content_type
            else convert_from_bytes(jd_file_content)
        )
    ]
    for file in files:
        file_content = file.file.read()
        encoded_resumes = [
            image_to_base64(content)
            for content in (
                [Image.open(BytesIO(file_content))]
                if "image" in file.content_type
                else convert_from_bytes(file_content)
            )
        ]
        existing = crud.application.get_multi_by_owner(db=db, owner_id=current_user.id)
        # Check if the application is already in the database
        hash_images = hashlib.md5(str(encoded_resumes).encode("utf-8")).hexdigest()
        hash_jd_images = hashlib.md5(str(encoded_jd).encode("utf-8")).hexdigest()
        for ex in existing:
            hash_ex_resume = hashlib.md5(str(ex.resume).encode("utf-8")).hexdigest()
            hash_ex_jd = hashlib.md5(
                str(ex.job_description).encode("utf-8")
            ).hexdigest()
            if hash_ex_resume == hash_images and hash_ex_jd == hash_jd_images:
                return ex

        try:
            task = celery_app.send_task(
                "app.worker.process_resume", args=[encoded_resumes, encoded_jd]
            )
            print("Sent the task")
            details = task.get()
            obj_in = schemas.ApplicationCreate(
                **details
            )
            # Create the application
            crud.application.create_with_owner(
                db=db, obj_in=obj_in, owner_id=current_user.id
            )
            print("Finished the task")
        except Exception as e:
            print(f"Error: {e}")
            return HTTPException(status_code=400, detail="Error processing resume")
    return status.HTTP_200_OK


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
    if not crud.user.is_admin(current_user) and (
        application.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    application = crud.application.update(
        db=db, db_obj=application, obj_in=application_in
    )
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
    if not crud.user.is_admin(current_user) and (
        application.owner_id != current_user.id
    ):
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
    if not crud.user.is_admin(current_user) and (
        application.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    application = crud.application.remove(db=db, id=id)
    return application


@router.post("/send-emails/{top_k}")
def send_mails(
    *,
    db: Session = Depends(deps.get_db),
    top_k: int = 5,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Send email to the top k candidates based on score on application.
    """
    applications = crud.application.get_multi_by_owner(db=db, owner_id=current_user.id)
    applications = [app for app in applications if app.score > 0.65]
    applications = sorted(applications, key=lambda x: x.score, reverse=True)
    applications = applications[:top_k]
    try:
        for application in applications:
            email_to = application.name
            if not validate_email(email_to):
                continue
            email_from = current_user.email
            subject = "Interview Invitation: Congratulations on Being Shortlisted!"
            message = f"""
                    We are excited to inform you that you have been shortlisted for the upcoming interview. Congratulations on reaching this stage of our selection process!
                    To schedule an interview or provide your availability, please use the following link: https://calendly.com/collinson-group/25-min-interview

                    We look forward to getting to know you better and discussing your qualifications in more detail. If you have any questions or need further assistance, please do not hesitate to contact us.
                    Thank you for your interest in joining our team, and we hope to see you soon!

                    Best regards,  
                    {current_user.full_name} 
                    {current_user.email}
                    """
            send_email(email_from, email_to, subject, message)
        return status.HTTP_200_OK
    except Exception as e:
        return HTTPException(status_code=400, detail="Error sending email")


@router.post("/send-email")
def send_mail(
    *,
    email_to: List[str],
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    try:
        for mail in email_to:
            if not validate_email(mail):
                continue
            email_to = mail
            email_from = current_user.email
            subject = "Interview Invitation: Congratulations on Being Shortlisted!"
            message = f"""
                We are excited to inform you that you have been shortlisted for the upcoming interview. Congratulations on reaching this stage of our selection process!
                To schedule an interview or provide your availability, please use the following link: https://calendly.com/collinson-group/25-min-interview

                We look forward to getting to know you better and discussing your qualifications in more detail. If you have any questions or need further assistance, please do not hesitate to contact us.
                Thank you for your interest in joining our team, and we hope to see you soon!

                Best regards, 
                {current_user.full_name} 
                {current_user.email}
                """
            send_email(email_from, email_to, subject, message)
        return status.HTTP_200_OK
    except Exception as e:
        return HTTPException(status_code=400, detail="Error sending email")


@router.post("/download/{id}")
def download(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    application = crud.application.get(db=db, id=id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    try:
        image = download_pdf(application.records)
        pdf = image_to_pdf(image)
        headers = {
            "Content-Disposition":  f"attachment; filename=score.pdf"
        }  
        return FileResponse(pdf, media_type="application/pdf", headers=headers)

    except Exception as e:
        print(e)
        return HTTPException(status_code=400, detail="Error downloading file")
