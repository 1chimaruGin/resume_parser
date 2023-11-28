import json
from raven import Client
from typing import List
from app.core.celery_app import celery_app
from app.core.config import settings
from app.lib.match import Matcher


_matcher = Matcher()

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task(acks_late=True)
def process_resume(images: List[str], file_names: List[str], job_description: str, num_process: int = 4) -> bool:
    outputs = _matcher.process(images, job_description, file_names, num_process)
    processed_outputs = {}
    for resume, jobd, details, file_name in outputs:
        try:
            details = json.loads(details)
        except json.decoder.JSONDecodeError:
            processed_outputs[file_name] = "Error"
            continue
        processed_outputs[file_name] = {
            "name": details["name"],
            "score": details["score"],
            "records": details,
            "is_ready": True,
            "resume": resume,
            "job_description": jobd,
        }
    # Process the resume
    # _, _, similarity, details = _matcher.process(images, jd_images)
    # try:
    #     details = json.loads(details)
    # except json.decoder.JSONDecodeError:
    #     details = ast.literal_eval(details)
    # obj_in = {
    #     "name": details["name"],
    #     "score": similarity,
    #     "records": details,
    #     "is_ready": True,
    #     "resume": images,
    #     "job_description": jd_images,
    # }
    # return obj_in
