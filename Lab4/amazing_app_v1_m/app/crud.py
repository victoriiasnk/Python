from typing import Union, Optional

from app import models
from app import schemes
from typing import Optional

from sqlalchemy.orm import Session

import hashlib


def create_user(db: Session, user: schemes.UserCreate) -> schemes.User:
    hashed_password = hashlib.md5(user.password.encode())
    db_user = models.User(email=user.email, first_name=user.first_name,
                          second_name=user.second_name, password=hashed_password.hexdigest())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def create_user_record(db: Session, db_record: models.Record, user_id: int) -> models.Record:
    db_record.user_id = user_id
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def create_record(db: Session, record: schemes.RecordCreate) -> schemes.Record:
    db_record = models.Record(date=record.date, title=record.title,
                              content=record.content)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_record_by_id(db, record_id: int):
    return db.query(models.Record).filter(models.Record.id == record_id).first()


def get_user_records(db: Session, user_id: int) -> list[models.Record]:
    return db.query(models.Record).filter(models.Record.user_id == user_id).all()


def get_record(db: Session, record_id: int) -> Optional[models.Record]:
    return db.query(models.Record).filter(models.Record.id == record_id).first()


def get_record_by_content(db: Session, content: str) -> Optional[models.Record]:
    return db.query(models.Record).filter(models.Record.content == content).first()

def update_user(db: Session, user_id: int, user_data: schemes.UserBase) -> Optional[schemes.User]:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in user_data.dict().items():
            if value is not None:
                setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def update_record(db: Session, record_id: int, updated_record: schemes.RecordBase) -> Optional[schemes.Record]:
    db_record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if db_record:
        for key, value in updated_record.dict().items():
            if value is not None:
                setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
        return db_record
    return None


def delete_record(db: Session, record_id: int) -> bool:
    db_record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if db_record:
        db.delete(db_record)  # Delete the record from the session
        db.commit()  # Commit the transaction to reflect the deletion in the database
        return True
    return False
