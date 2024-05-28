from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OpinionProject.settings')

app = Celery('OpinionProject')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-email-every-morning': {
        'task': 'onions.tasks.upload_highlight',
        'schedule': crontab(hour="7", minute="30"),
    },
}
