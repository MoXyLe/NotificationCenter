import os
import time
from celery import Celery
from db import SessionLocal, engine
from sqlalchemy.orm import Session
import models, schemas
from crud import get_mailing_list_by_task_id, create_and_get_messages, get_client_by_id
import requests
from requests.structures import CaseInsensitiveDict


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(bind=True, name="create_task")
def create_mailing_task(self):
    time.sleep(2)
    db = SessionLocal()
    mailing_list = get_mailing_list_by_task_id(db=db, task_id=self.request.id)
    db.close()
    if mailing_list:
        if mailing_list.start_time > time.time():
            time.sleep(mailing_list.start_time - time.time())
        elif mailing_list.finish_time < time.time():
            return "Too late to send mailing!"

        db = SessionLocal()
        messages = create_and_get_messages(db=db, mailing_list=mailing_list)

        time_is_up = False

        for i in messages:
            if time.time() > mailing_list.finish_time:
                time_is_up = True
                break
            url = "https://probe.fbrq.cloud/v1/send/" + str(i.id)

            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            headers["Authorization"] = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODE5ODIyOTgsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IlZpa3RvciJ9.99s3rne8bfaASiw5LYVNglDWM-oQtt5opK1lLKdZWF4"
            headers["Content-Type"] = "application/json"

            data='{"id": ' + str(i.id) + ', "phone": ' + str(i.client.phone_number) + ', "text": "' + str(mailing_list.text) + '"}'

            resp = requests.post(url, headers=headers, data=data, timeout=15)

            if resp.status_code == 200:
                #message = db.query(models.Message).filter(models.Message.id == i.id).first()
                #message.status = True
                i.sent = True

        db.commit()
        db.close()

        if time_is_up:
            return "Time ran out!"
        else:
            return "Finish sending emails"
    else:
        return "No mailing_list with task_id = " + str(self.request.id)
