#from __future__ import absolute_import, unicode_literals
import time

from celery import shared_task
from celery.utils.log import get_task_logger
from wood_export_bot.celery import app as celery_app
from wood_export_bot.celery import app
from celery.schedules import crontab
from .bot_init import bot
from .models import Document, DocumentsInApplication
import uuid
from celery import chord

logger = get_task_logger(__name__)

@app.task
def supper_sum(x,y):
    #time.sleep(10)
    print("F + F + F + F")
    bot.send_message(630157933, "BACK TASK")
    print(x + y)



