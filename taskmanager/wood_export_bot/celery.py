import os
import datetime
from celery import Celery
from celery.schedules import crontab
#from main.tasks import supper_sum
#from wood_export_bot.celery import show

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wood_export_bot.settings")
app = Celery("wood_export_bot")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

#task = app.task

