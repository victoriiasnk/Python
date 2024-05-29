from pydantic import BaseModel

from datetime import date, datetime


class RecordBase(BaseModel):
    date: date
    title: str
    content: str


class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    first_name: str
    second_name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    records: list[Record] = []

    class Config:
        orm_mode = True


class RequestDetails(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class ChangePassword(BaseModel):
    email: str
    old_password: str
    new_password: str


class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime
