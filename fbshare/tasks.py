from .fbshare import fb_data
from celery import shared_task
@shared_task
def get_fb_data() :
    fb_data()

    return "run successful"

