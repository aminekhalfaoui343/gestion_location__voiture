from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from dotenv import load_dotenv
import os

from api.models import Admin, Renter
from api.deps import db_dependency, bcrypt_context

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")

# ============================
#           SCHEMAS
# ============================

class AdminCreateRequest(BaseModel):
    username: str
    password: str

class UserCreateRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


# ============================
#        AUTH FUNCTIONS
# ============================

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    payload = {
        "sub": username,
        "id": user_id,
        "exp": datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# -------- ADMIN AUTH --------

def authenticate_admin(username: str, password: str, db):
    admin = db.query(Admin).filter(Admin.username == username).first()

    if not admin:
        return False

    if not bcrypt_context.verify(password, admin.hashed_password):
        return False

    return admin


# -------- USER AUTH --------

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user


# ============================
#        ROUTES ADMIN
# ============================

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

    return {"access_token": token, "token_type": "bearer"}


# ============================
#        ROUTES USER
# ============================

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: UserCreateRequest):

    new_user = User(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created successfully ✅"}


@router.post('/token', response_model=Token)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    token = create_access_token(
        user.username,
        user.id,
        timedelta(minutes=20)
    )

    return {"access_token": token, "token_type": "bearer"}
