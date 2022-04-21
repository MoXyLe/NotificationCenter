from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class MailingList(Base):
    __tablename__ = "mailing_list"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(Integer)
    text = Column(String)
    filter = Column(String)
    finish_time = Column(Integer)
    task_id = Column(String)

    message = relationship("Message", back_populates="mailing_list")


class Client(Base):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(Integer, unique=True, index=True)
    operator = Column(Integer)
    tag = Column(String)
    timezone = Column(Integer)

    message = relationship("Message", back_populates="client")

class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    send_time = Column(Integer)
    sent = Column(Boolean)
    mailing_id = Column(Integer, ForeignKey("mailing_list.id"))
    client_id = Column(Integer, ForeignKey("client.id"))

    mailing_list = relationship("MailingList", back_populates="message")
    client = relationship("Client", back_populates="message")
