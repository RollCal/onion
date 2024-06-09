from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OpinionProject.settings')

app = Celery('OpinionProject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    result_expires=timedelta(days=1),
)

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'upload_highlight_every_': {
        'task': 'onions.tasks.upload_highlight',
        'schedule': crontab(minute="*/10"),
    },
}
