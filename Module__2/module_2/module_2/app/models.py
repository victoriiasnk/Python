from sqlalchemy import Column, ForeignKey, String, Integer, Date, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.database import Base

import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, index=True)
    second_name = Column(String, index=True)
    email = Column(String, unique=True)
    password = Column(String)

    records = relationship("Record", back_populates="user")


class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="records", cascade="all, delete")


class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    refresh_toke = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)