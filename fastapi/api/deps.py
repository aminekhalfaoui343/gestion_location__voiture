from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

# Import propre
from api.database import SessionLocal

load_dotenv()

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")

# ============================
#       DATABASE DEPENDENCY
# ============================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# ============================
#       SECURITY SETUP
# ============================

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Ce tokenUrl = '/auth/token' correspond à la route User
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

oauth2_bearer_dependency = Annotated[str, Depends(oauth2_bearer)]


# ============================
#       JWT VALIDATION
# ============================

async def get_current_user(token: oauth2_bearer_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user"
            )

        return {"username": username, "id": user_id}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user"
        )


user_dependency = Annotated[dict, Depends(get_current_user)]
