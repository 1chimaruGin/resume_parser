import json
from PIL import Image
from raven import Client
from app.core.celery_app import celery_app
from app.core.config import settings
from app.lib.match import Matcher

_matcher = Matcher()

client_sentry = Client(settings.SENTRY_DSN)
@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"

@celery_app.task(acks_late=True)
def process_resume(images: str, job_title: str, industry: str, job_description: str) -> str:
    resume, simi, records = _matcher.process(images, job_title, industry, job_description)
    records = json.loads(records)
    return {
        "name": records["name"],
        "resume_text": resume,
        "score": simi,
        "records": records,
        "is_ready": True
    }

@celery_app.task(acks_late=True)
def send_email(email_to):
    pass