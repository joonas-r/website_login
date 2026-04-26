from sqlalchemy.orm import Session
from auth import hash_password
from models import User



def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.username == name).first()


def create_user(db: Session, username: str, password: str):
    user = User(
        username=username,
        password_hash=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

