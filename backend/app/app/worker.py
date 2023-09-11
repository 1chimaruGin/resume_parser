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
def process_resume(images: Image.Image, job_description) -> str:
    print("The task received")
    resume, simi, records = _matcher.process(images, job_description)
    return {
        "resume": resume,
        "simiarity": simi,
        "records": records
    }