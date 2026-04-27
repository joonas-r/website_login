from fastapi import FastAPI, Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

from database import engine, get_db, Base
from models import User, Match, Team
import crud
from auth import hash_password, verify_password, create_access_token, get_current_user
from schemas import CreateUser, LoginRequest, ReadMatches, CreateMatch, PatchMatchScore, ReadTeamStats, PatchTeamStats

app = FastAPI()

# router = APIRouter(
#     prefix="",
#     dependencies=[Depends(get_current_user)],
# )

# app.include_router(router)


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

@app.post("/matches")
def create_match_route(
    match: CreateMatch,
    db: Session = Depends(get_db)
):
    return crud.create_match(db, match)


@app.patch("/matches/{match_id}", response_model=ReadMatches)
def patch_match_score(
    match_id: int,
    updates: PatchMatchScore,
    db: Session = Depends(get_db),
):
    match = db.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    return crud.update_match_score(db, match, updates)


@app.delete("/matches/{match_id}", status_code=204)
def delete_match(
    match_id: int,
    db: Session = Depends(get_db),
    # user: User = Depends(get_current_user),  # auth protection
):
    match = db.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    crud.delete_match(db, match)

@app.get("/teams", response_model=list[ReadTeamStats])
def read_teams(
    db: Session = Depends(get_db)
):
    return crud.get_all_team_stats(db)

@app.patch("/teams/{team_id}", response_model=ReadTeamStats)
def patch_team_stats(
    team_id: int,
    updates: PatchTeamStats,
    db: Session = Depends(get_db),
):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    return crud.update_team_stats(db, team, updates)