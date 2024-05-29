from app import schemes, crud
from app.database import get_db
from app.ml import *
from app.auth_bearer import JWTBearer

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

records_router = APIRouter(prefix="/records", tags=["records"])


@records_router.post("/", response_model=schemes.Record)
def create_user_record(record: schemes.RecordCreate, user_id: int, db: Session = Depends(get_db), dependencies=Depends(JWTBearer())):
    db_record = crud.create_user_record(db, item=record, user_id=user_id)
    return db_record
    # 1. Are there new tokens
    # 2. update_model()
    # 3. gen_embeddings(new_record)
    # 4. store record_id -> embedding in a new SQL table
    # [record_id, embeddings: JSON]
    # embeddings: list[numpy.arrays] -> JSON

@records_router.get("/{record_id}", response_model=schemes.Record)
def get_record(record_id: int, db: Session = Depends(get_db), dependencies=Depends(JWTBearer())):
    record_id = crud.get_record_by_id(db, id=record_id)
    if record_id is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record_id

@records_router.put("/{record_id}", response_model=schemes.Record)
def update_record(record_id: int, db: Session = Depends(get_db), dependencies=Depends(JWTBearer())):
    record = crud.get_record_by_id(db, id=record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    record = crud.update_record(db, record=record)
    return record

# @users_router.put("/{user_id}", response_model=schemes.User)
# def update_user(user_id: int, user: schemes.UserBase, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     db_user = crud.update_user(db, user=user)
#     return db_user