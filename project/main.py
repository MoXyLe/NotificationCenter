from celery.result import AsyncResult
from celery.task.control import revoke

from fastapi import Body, FastAPI, Form, Request, HTTPException, Depends


from typing import Optional, List, Dict, Tuple
from sqlalchemy.orm import Session
import time

import crud, models, schemas
from db import SessionLocal, engine
from worker import create_mailing_task


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/new_client/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    if len(str(client.phone_number)) < 10:
        raise HTTPException(status_code=400, detail="Phone number is wrong")
    db_client = crud.get_client(db=db, client_phone=client.phone_number)
    if db_client:
        raise HTTPException(status_code=400, detail="Client already registered")
    return crud.create_client(db=db, client=client)


@app.put("/client/{client_id}", response_model=schemas.Client)
def update_client(client_id: int, phone_number: Optional[int] = None, tag: Optional[str] = None, timezone: Optional[int] = None, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_id(db=db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=400, detail="Client does not exist")
    new_attrs = dict()
    if phone_number:
        if len(str(phone_number)) >= 10:
            new_attrs["phone_number"] = phone_number
        else:
            raise HTTPException(status_code=400, detail="Phone number is wrong")
    if tag:
        new_attrs["tag"] = tag
    if timezone:
        new_attrs["timezone"] = timezone
    return crud.update_client(db=db, client_id=client_id, new_attrs=new_attrs)


@app.delete("/client/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_id(db=db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return crud.delete_client(db=db, client_id=client_id)


@app.post("/new_mailing_list/", response_model=schemas.MailingList)
def create_mailing_list(mailing_list: schemas.MailingListBase, db: Session = Depends(get_db)):
    if mailing_list.start_time > mailing_list.finish_time or mailing_list.finish_time < time.time():
        raise HTTPException(status_code=400, detail="Wrong time!")
    task = create_mailing_task.delay()
    new_mailing_list = crud.create_mailing_list(db=db, mailing_list=mailing_list, task_id=task.id)
    return new_mailing_list


@app.put("/mailing_list/{mailing_list_id}", response_model=schemas.MailingList)
def update_mailing_list(mailing_list_id: int, start_time: Optional[int] = None, text: Optional[str] = None, filter: Optional[str] = None, finish_time: Optional[int] = None, db: Session = Depends(get_db)):
    db_mailing_list = crud.get_mailing_list_by_id(db=db, mailing_list_id=mailing_list_id)
    if db_mailing_list is None:
        raise HTTPException(status_code=400, detail="MailingList does not exist")
    new_attrs = dict()
    if start_time:
        if finish_time:
            if start_time > finish_time or finish_time < time.time():
                raise HTTPException(status_code=400, detail="Wrong time!")
            new_attrs["start_time"] = start_time
            new_attrs["finish_time"] = finish_time
        else:
            if start_time > db_mailing_list.finish_time:
                raise HTTPException(status_code=400, detail="Wrong time!")
            else:
                new_attrs["start_time"] = start_time
    elif finish_time:
        if finish_time < time.time() or db_mailing_list.start_time > finish_time:
            raise HTTPException(status_code=400, detail="Wrong time!")
    if text:
        new_attrs["text"] = text
    if filter:
        new_attrs["filter"] = filter
    revoke(db_mailing_list.task_id, terminate=True)
    task = create_mailing_task.delay()
    new_attrs["task_id"] = task.id
    return crud.update_mailing_list(db=db, mailing_list_id=mailing_list_id, new_attrs=new_attrs)


@app.delete("/mailing_list/{mailing_list_id}")
def delete_mailing_list(mailing_list_id: int, db: Session = Depends(get_db)):
    db_mailing_list = crud.get_mailing_list_by_id(db=db, mailing_list_id=mailing_list_id)
    if db_mailing_list is None:
        raise HTTPException(status_code=404, detail="MailingList not found")
    return crud.delete_mailing_list(db=db, mailing_list_id=mailing_list_id)


@app.get("/message_stats/", response_model=List[schemas.Message])
def get_message_stats(db: Session = Depends(get_db)):
    stats = crud.get_message_stats(db=db)
    messages_list = list()
    for i in stats:
        messages_list.append(i)
    return messages_list


@app.get("/mailing_stats/", response_model=List[schemas.MailingListStats])
def get_mailing_stats(db: Session = Depends(get_db)):
    mailings = crud.get_mailing_stats(db=db)
    mailing_dict = dict()
    for i in mailings:
        mailing_dict[i.id] = len(i.message)
    mailing_dict = dict(sorted(mailing_dict.items(), key=lambda item: item[1], reverse=True))
    mailing_list = list()
    for key, value in mailing_dict.items():
        cur_mailing = crud.get_mailing_list_by_id(db=db, mailing_list_id=key)
        cur_mailing.amount_of_messages = value
        mailing_list.append(cur_mailing)
    return mailing_list

@app.get("/mailing_stats/{mailing_id}/", response_model=List[schemas.Message])
def get_messages_for_mailing(mailing_id: int, db: Session = Depends(get_db)):
    stats = crud.get_mailing_list_by_id(db=db, mailing_list_id=mailing_id)
    if stats:
        return stats.message
    else:
        raise HTTPException(status_code=404, detail="MailingList not found")
