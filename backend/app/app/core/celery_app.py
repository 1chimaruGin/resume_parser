from celery import Celery

BROKER_URL = "pyamqp://guest:guest@queue:5672//"
RESULT_BACKEND = "rpc://guest:guest@queue:5672//"

celery_app = Celery("worker", broker=BROKER_URL, backend=RESULT_BACKEND)
celery_app.conf.task_routes = {
    "app.worker.test_celery": "main-queue",
    "app.worker.process_resume": "main-queue",
}

# celery_app.config_from_object('your_project.celery_config')
