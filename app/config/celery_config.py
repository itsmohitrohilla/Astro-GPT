from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',  # broker
    backend='redis://localhost:6379/0'  # backend
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

celery_app.autodiscover_tasks(['app.services.astro_gpt'])