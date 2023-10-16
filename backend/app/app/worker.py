import json
import hashlib
from raven import Client
from typing import List
from sqlalchemy.orm import Session
from app.core.celery_app import celery_app
from app.core.config import settings
from app.lib.match import Matcher
from app import crud, models, schemas


_matcher = Matcher()

client_sentry = Client(settings.SENTRY_DSN)
@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"

@celery_app.task(acks_late=True)
def process_resume(images: List[str], jd_images: List[str], db: Session, current_user: models.User) -> bool:
    existing = crud.application.get_multi_by_owner(
        db=db, owner_id=current_user.id
    )
    # Check if the application is already in the database
    hash_images = hashlib.md5(str(images).encode("utf-8")).hexdigest()
    hash_jd_images = hashlib.md5(str(jd_images).encode("utf-8")).hexdigest()
    for ex in existing:
        hash_ex_resume = hashlib.md5(str(ex.resume).encode("utf-8")).hexdigest()
        hash_ex_jd = hashlib.md5(str(ex.job_description).encode("utf-8")).hexdigest()
        if hash_ex_resume == hash_images and hash_ex_jd == hash_jd_images:
            print("[INFO] The job application is already in the database")
            return ex
    
    # Process the resume
    resume, job_description, similarity, details = _matcher.process(images, jd_images)
    details = json.loads(details)
    details["score"] = similarity
    obj_in = schemas.ApplicationCreate(resume=resume, job_description=job_description, **details)

    # Create the application
    crud.application.create_with_owner(
        db=db, 
        obj_in=obj_in,
        owner_id=current_user.id
    )
    
    return True