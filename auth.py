from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, Cookie, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User

SECRET_KEY = "fgiu?4239345!"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_access_token(user_id: int):
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)



def get_current_user(
    access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=401)

    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    user = db.get(User, payload["sub"])

    if not user:
        raise HTTPException(status_code=401)

    return user



