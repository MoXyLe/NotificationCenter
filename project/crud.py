from sqlalchemy.orm import Session
import models, schemas
import time


def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(phone_number=client.phone_number, operator=int(str(client.phone_number)[1:4]), tag=client.tag, timezone=client.timezone)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def update_client(db: Session, client_id: int, new_attrs: dict):
    db_client = db.query(models.Client).filter(models.Client.id == client_id)
    if "phone_number" in new_attrs:
        db_client.update({"phone_number" : new_attrs["phone_number"], "operator" : int(str(new_attrs["phone_number"])[1:4])}, synchronize_session="fetch")
    if "tag" in new_attrs:
        db_client.update({"tag" : new_attrs["tag"]}, synchronize_session="fetch")
    if "timezone" in new_attrs:
        db_client.update({"timezone" : new_attrs["timezone"]}, synchronize_session="fetch")
    db.commit()
    return db_client.first()


def delete_client(db: Session, client_id: int):
    db_client = db.query(models.Client).filter(models.Client.id == client_id).delete(synchronize_session="fetch")
    db.commit()
    return "Success"


def get_client(db: Session, client_phone: int):
    return db.query(models.Client).filter(models.Client.phone_number == client_phone).first()


def get_client_by_id(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def create_mailing_list(db: Session, mailing_list: schemas.MailingListBase, task_id):
    db_mailing_list = models.MailingList(start_time=mailing_list.start_time, text=mailing_list.text, filter=mailing_list.filter, finish_time=mailing_list.finish_time, task_id=task_id)
    db.add(db_mailing_list)
    db.commit()
    db.refresh(db_mailing_list)
    return db_mailing_list


def update_mailing_list(db: Session, mailing_list_id: int, new_attrs: dict):
    db_mailing_list = db.query(models.MailingList).filter(models.MailingList.id == mailing_list_id)
    if "start_time" in new_attrs:
        db_mailing_list.update({"start_time" : new_attrs["start_time"]}, synchronize_session="fetch")
    if "text" in new_attrs:
        db_mailing_list.update({"text" : new_attrs["text"]}, synchronize_session="fetch")
    if "filter" in new_attrs:
        db_mailing_list.update({"filter" : new_attrs["filter"]}, synchronize_session="fetch")
    if "finish_time" in new_attrs:
        db_mailing_list.update({"finish_time" : new_attrs["finish_time"]}, synchronize_session="fetch")
    if "task_id" in new_attrs:
        db_mailing_list.update({"task_id" : new_attrs["task_id"]}, synchronize_session="fetch")
    db.commit()
    return db_mailing_list.first()


def delete_mailing_list(db: Session, mailing_list_id: int):
    db_mailing_list = db.query(models.MailingList).filter(models.MailingList.id == mailing_list_id).delete(synchronize_session="fetch")
    db.commit()
    return "Success"


def get_mailing_list_by_id(db: Session, mailing_list_id: int):
    return db.query(models.MailingList).filter(models.MailingList.id == mailing_list_id).first()


def get_mailing_list_by_task_id(db: Session, task_id: int):
    return db.query(models.MailingList).filter(models.MailingList.task_id == task_id).first()


def get_message_stats(db: Session):
    return db.query(models.Message).order_by(models.Message.mailing_id.desc())


def get_mailing_stats(db: Session):
    return db.query(models.MailingList)


def create_and_get_messages(db: Session, mailing_list: models.MailingList):
    clients = db.query(models.Client).filter(models.Client.tag == mailing_list.filter)
    try:
        operator = int(mailing_list.filter)
        clients = db.query(models.Client).filter(models.Client.operator == operator)
    except:
        pass
    messages = list()
    for i in clients:
        db_message = models.Message(send_time=time.time(), sent=False, mailing_id=mailing_list.id, client_id=i.id)
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        messages.append(db_message)
    return messages
