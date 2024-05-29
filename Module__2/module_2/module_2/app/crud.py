from typing import Optional
import json
from datetime import date

from app import models
from app import schemes

from sqlalchemy.orm import Session

import hashlib


def create_user(db: Session, user: schemes.UserCreate) -> schemes.User:
    db_user = models.User(email=user.email, first_name=user.first_name,
                          second_name=user.second_name, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_record(db: Session, item: schemes.RecordCreate, user_id: int) -> schemes.Record:
    db_record = models.Record(date=item.date, title=item.title, content=item.content, user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_user(db: Session, user: schemes.UserCreate) -> schemes.Record:
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    db_user.first_name = user.first_name
    db_user.second_name = user.second_name
    db_user.email = user.email
    db.commit()
    return db_user

def update_record(db: Session, record: schemes.RecordCreate) -> schemes.Record:
    db_record = db.query(models.Record).filter(models.Record.id == record.id).first()
    db_record.content = record.content
    db.commit()
    return db_record


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def get_record_by_id(db: Session, id: int) -> Optional[models.Record]:
    return db.query(models.Record).filter(models.Record.id == id).first()

def get_all_records(db: Session):
    return db.query(models.Record).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()