from celery import shared_task
from OpinionProject import settings

@shared_task
def db_integrity_check():
    pass