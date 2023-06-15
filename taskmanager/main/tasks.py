#from __future__ import absolute_import, unicode_literals
from datetime import datetime, timedelta, date

import pytz
from pytz import timezone

from celery import shared_task
from celery.utils.log import get_task_logger
from wood_export_bot.celery import app as celery_app
from wood_export_bot.celery import app
from celery.schedules import crontab
from .bot_init import bot
from .models import DocumentsInApplicationForPayment, DocumentsInApplicationArchive, ApplicationArchive, ApplicationForPayment
import uuid
from celery import chord

logger = get_task_logger(__name__)

@app.task
def supper_sum(x):
    #time.sleep(10)
    print("F + F + F + F")
    #bot.send_message(630157933, "BACK TASK")
    print(x)



@app.task
def show():
    print("FFFFFFF")

@app.task
def benefit_status_schedule(date, app_id):
    payment_day = datetime.utcnow() + timedelta(minutes=1)
    change_benefit_status.apply_async((app_id,), eta=payment_day)

#show.apply_async(eta=datetime.datetime(2023, 6, 9, 16, 17)) #y/m/d

#CHANGE BENEFIT APP STATUS WHEN IT' DONE
#def benefit_status_schedule(date):
#    app.conf.beat_schedule = {
#        'task-name': {
#            # 'task': 'wood_export_bot.celery',  # instead 'show'
#            'task': 'main.tasks.supper_sum',
#            'schedule': 5,
#            'args': (42,),
#        },
#    }


@app.task
def change_benefit_status(app_id):
    app = ApplicationForPayment.objects.filter(id=app_id).first()

    if app.state == "PM":
        app_archive = ApplicationArchive.objects.create(
            chat_id=app.chat_id,
            created=app.created,
            fio=app.fio,
            benefit=app.benefit,
            state='P',
            sum=app.sum
        )

        documents = DocumentsInApplicationForPayment.objects.filter(application_payment_id=app_id).all()

        for document in documents:
            DocumentsInApplicationArchive.objects.create(application_archive_id=app_archive.pk, document_id=document.pk)



        app.delete()


app.conf.timezone = 'UTC'
