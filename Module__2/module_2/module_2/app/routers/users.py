from app import schemes, crud
from app.database import get_db
from app.models import TokenTable
from app.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token
from app.auth_bearer import JWTBearer
from jose import jwt
import json
from app.ml.word2vec import find_similar_records

from fastapi import FastAPI, Query, APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session
from datetime import datetime


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"   # should be kept secret
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"


users_router = APIRouter(prefix="/users", tags=["users"])

# "http//:localhost:8000/users"


@users_router.post("/", response_model=schemes.User)
def create_user(user: schemes.UserCreate, db: Session = Depends(get_db)) -> schemes.User:
    # parse string -> user = dict...
    # db_user = crud.create_user(db, user=user)
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail=f"User with email={user.email} already exists")

    db_user = crud.create_user(db, user=user)
    return db_user


@users_router.get("/{user_id}", response_model=schemes.User)
def get_user(user_id: int, db: Session = Depends(get_db), dependencies=Depends(JWTBearer())):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users_router.get("/{email}", response_model=schemes.User)
def get_user_email(email: str, db: Session = Depends(get_db), dependencies=Depends(JWTBearer())):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@users_router.put("/{user_id}", response_model=schemes.User)
def update_user(user_id: int, user: schemes.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = crud.update_user(db, user=user)
    return db_user


@users_router.post("/register")
def register_user(user: schemes.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = get_hashed_password(user.password)

    user.password = encrypted_password
    print(user.password)
    crud.create_user(db, user=user)

    return {"message": "user created successfully"}


@users_router.post('/login', response_model=schemes.TokenSchema)
def login(request: schemes.RequestDetails, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=request.email)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    from passlib.context import CryptContext
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    print(password_context.hash(request.password))
    hashed_pass = db_user.password
    print(hashed_pass)
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    access = create_access_token(db_user.id)
    refresh = create_refresh_token(db_user.id)

    token_db = TokenTable(user_id=db_user.id, access_toke=access, refresh_toke=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }


@users_router.post('/change-password')
def change_password(request: schemes.ChangePassword, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=request.email)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if not verify_password(request.old_password, db_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

    encrypted_password = get_hashed_password(request.new_password)
    db_user.password = encrypted_password
    db.commit()
    return {"message": "Password changed successfully"}


@users_router.post('/logout')
def logout(dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    token = dependencies
    print(token)
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload['sub']
    token_record = db.query(TokenTable).all()
    info = []
    for record in token_record:
        print("record", record)
        if (datetime.utcnow() - record.created_date).days > 1:
            info.append(record.user_id)
    if info:
        existing_token = db.query(TokenTable).where(TokenTable.user_id.in_(info)).delete()
        db.commit()

    existing_token = db.query(TokenTable).filter(TokenTable.user_id == user_id,
                                                 TokenTable.access_toke == token).first()
    if existing_token:
        existing_token.status = False
        db.add(existing_token)
        db.commit()
        db.refresh(existing_token)
    return {"message": "Logout Successfully"}


@users_router.get("/find_similar/")
def find_similar(user_id: int, record_id: int, db: Session = Depends(get_db), dependencies=Depends(JWTBearer())):
    db_records = crud.get_all_records(db)

    user_records = []
    other_records = []

    for record in db_records:
        if record.user_id == user_id and record.id == record_id:
            user_records.append(json.loads(record.content))
        else:
            other_records.append(json.loads(record.content))

    if len(user_records) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Records not found")

    familiar = find_similar_records(user_records, other_records)
    print(familiar)
    
    return familiar
    # user_record = user_record_from_database()
    # get all records from all users
    # find most similar to user_record based on embeddings from SQL table (records_id -> embeddings)
    # return most similar record based on cosine similarity