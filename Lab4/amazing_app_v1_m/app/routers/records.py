from app import schemes, crud
from app.database import get_db
# from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

records_router = APIRouter(prefix="/records", tags=["Records"])


@records_router.post("/", response_model=schemes.Record)
def create_record(record: schemes.RecordCreate, user_id: int, db: Session = Depends(get_db)) -> schemes.Record:
    db_record = crud.get_record_by_content(db, content=record.content)
    print(db_record)
    if db_record:
        raise HTTPException(status_code=400, detail=f"Record with content={record.content} already exists")

    db_record = crud.create_record(db=db, record=record)
    db_user_record = crud.create_user_record(db=db, db_record=db_record, user_id=user_id)
    return db_record


@records_router.get("/{record_id}", response_model=schemes.Record)
def read_record(record_id: int, user_id: int, db: Session = Depends(get_db)) -> schemes.Record:
    db_record = crud.get_record_by_id(db, record_id=record_id)
    if db_record:
        return db_record
    else:
        raise HTTPException(status_code=404, detail=f"Record with ID={record_id} not found for user with ID={user_id}")


@records_router.put("/{record_id}", response_model=schemes.Record)
def update_record(record_id: int, record_update: schemes.RecordBase, db: Session = Depends(get_db)) -> schemes.Record:
    db_record = crud.get_record_by_id(db, record_id=record_id)

    if db_record:
        crud.update_record(db, record_id=db_record.id, updated_record=record_update)

        db.commit()
        db.refresh(db_record)

        return db_record
    else:
        raise HTTPException(status_code=404, detail=f"Record with ID={record_id} not found")


@records_router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)) -> None:
    db_record = crud.get_record_by_id(db, record_id=record_id)
    if db_record:
        crud.delete_record(db, record_id=db_record.id)

        db.commit()
        db.refresh(db_record)
    else:
        raise HTTPException(status_code=404, detail=f"Record with ID={record_id} not found")



#@records_router.get("/{record_id}", response_model=schemes.Record)
#def read_record(record_id: int, user_id: int, db: Session = Depends(get_db)) -> schemes.Record:
 #   db_record = crud.get_record_by_id(db, record_id=record_id, user_id=user_id)
  #  if db_record:
   #     return db_record
    #else:
     #   raise HTTPException(status_code=404, detail=f"Record with ID={record_id} not found for user with ID={user_id}")