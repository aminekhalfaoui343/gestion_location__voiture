from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from dotenv import load_dotenv
import os
<<<<<<< HEAD

from api.models import Admin
=======
from api.models import User
>>>>>>> 06f716055b3c6dd1cc385fbd15a6aa910770b7e9
from api.deps import db_dependency, bcrypt_context

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")

<<<<<<< HEAD

# ----------- SCHEMAS ------------

class AdminCreateRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# ----------- FUNCTIONS ------------

def authenticate_admin(username: str, password: str, db):
    admin = db.query(Admin).filter(Admin.username == username).first()

    if not admin:
        return False
    
    if not bcrypt_context.verify(password, admin.hashed_password):
        return False
    
    return admin


def create_access_token(username: str, admin_id: int, expires_delta: timedelta):
    payload = {
        'sub': username,
        'id': admin_id
    }
    expires = datetime.now(timezone.utc) + expires_delta
    payload.update({'exp': expires})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ----------- ROUTES ------------

@router.post("/admin", status_code=status.HTTP_201_CREATED)
async def create_admin(db: db_dependency, create_admin_request: AdminCreateRequest):

    new_admin = Admin(
        username=create_admin_request.username,
        hashed_password=bcrypt_context.hash(create_admin_request.password)
    )

    db.add(new_admin)
    db.commit()

    return {"message": "Admin created successfully ✅"}


@router.post('/admin/token', response_model=Token)
async def admin_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    admin = authenticate_admin(form_data.username, form_data.password, db)

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials"
        )

    token = create_access_token(
        admin.username,
        admin.id,
        timedelta(minutes=30)
    )

    return {'access_token': token, 'token_type': 'bearer'}
=======
class UserCreateRequest(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserCreateRequest):
    create_user_model = User(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )
    db.add(create_user_model)
    db.commit()
    
@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    
    return {'access_token': token, 'token_type': 'bearer'}
    
>>>>>>> 06f716055b3c6dd1cc385fbd15a6aa910770b7e9
