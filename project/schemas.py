from typing import List, Optional

from pydantic import BaseModel

class MailingListBase(BaseModel):
    start_time: int
    text: str
    filter: str
    finish_time: int

class MailingListCreate(MailingListBase):
    task_id: str

class MailingList(MailingListBase):
    id: int
    task_id: str

    class Config:
        orm_mode = True

class MailingListStats(MailingListBase):
    id: int
    task_id: str
    amount_of_messages: int

    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    phone_number: int
    tag: str
    timezone: int

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    operator: int

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    id: int
    send_time: int
    sent: bool
    mailing_id: int
    client_id: int

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):

    class Config:
        orm_mode = True
