from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

from database import engine, get_db, Base
from models import User 
import crud
from auth import hash_password, verify_password, create_access_token, get_current_user
from schemas import CreateUser, LoginRequest, ReadMatches

app = FastAPI()

Base.metadata.create_all(engine)

@app.post("/login")
def login(
#   username: str,
#    password: str,
    userdata: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == userdata.username).first()
    if not user or not verify_password(userdata.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.user_id)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
#        secure=True,     # HTTPS only
        samesite="lax"
    )

    return {"message": "Logged in"}


@app.get("/dashboard")
def dashboard(user: User = Depends(get_current_user)):
    return {"email": user.username}


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")

@app.post("/register", status_code=201)
def create_user_route(
    user: CreateUser,
    db: Session = Depends(get_db)
):
    existing = crud.get_user_by_name(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    crud.create_user(db, user.username, user.password)
    return {"message": "User created"}


@app.get("/matches", response_model=list[ReadMatches])
def read_matches(
    db: Session = Depends(get_db)
):
    return crud.get_all_matches(db)