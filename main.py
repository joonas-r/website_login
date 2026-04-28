from fastapi import FastAPI, Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware

from database import engine, get_db, Base
from models import User, Match, Team, PlayerStats
import crud
from auth import hash_password, verify_password, create_access_token, get_current_user
from schemas import CreateUser, LoginRequest, ReadMatches, CreateMatch, PatchMatchScore, ReadTeamStats, PatchTeamStats, ReadPlayerTeamInfo, ReadPlayerStats, PatchPlayerStats


app = FastAPI()

## Routers

matches_router = APIRouter(
    prefix="/matches",
    tags="[matches]",
    dependencies=[Depends(get_current_user)]
)

teams_router = APIRouter(
    prefix="/teams",
    tags=["teams"],
    dependencies=[Depends(get_current_user)]
)

players_router = APIRouter(
    prefix="/players",
    tags=["players"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(matches_router)
app.include_router(teams_router)
app.include_router(players_router)

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


@matches_router.get("", response_model=list[ReadMatches])
def read_matches(
    db: Session = Depends(get_db)
):
    return crud.get_all_matches(db)

@matches_router.post("")
def create_match_route(
    match: CreateMatch,
    db: Session = Depends(get_db)
):
    return crud.create_match(db, match)


@matches_router.patch("/{match_id}", response_model=ReadMatches)
def patch_match_score(
    match_id: int,
    updates: PatchMatchScore,
    db: Session = Depends(get_db),
):
    match = db.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    return crud.update_match_score(db, match, updates)


@matches_router.delete("/{match_id}", status_code=204)
def delete_match(
    match_id: int,
    db: Session = Depends(get_db),
    # user: User = Depends(get_current_user),  # auth protection
):
    match = db.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    crud.delete_match(db, match)

@teams_router.get("", response_model=list[ReadTeamStats])
def read_teams(
    db: Session = Depends(get_db)
):
    return crud.get_all_team_stats(db)

@teams_router.patch("/{team_id}", response_model=ReadTeamStats)
def patch_team_stats(
    team_id: int,
    updates: PatchTeamStats,
    db: Session = Depends(get_db),
):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    return crud.update_team_stats(db, team, updates)

@players_router.get("/team/{team_id}", response_model=list[ReadPlayerTeamInfo])
def read_team_players(
    team_id: int,    
    db: Session = Depends(get_db)
):
    players = crud.get_players_with_teams(db, team_id)

    return [
        {
            "player_id": p.player_id,
            "name": p.name,
            "shirt_number": p.shirt_number,
            "team_name": p.team.team_name if p.team else None,
        }
        for p in players
    ]

@players_router.get("/{player_id}/stats", response_model=ReadPlayerStats)
def read_player_stats(
    player_id: int,
    db: Session = Depends(get_db)
):
    player_stats = crud.get_player_stats(db, player_id)
    return {
            "player_id": player_stats.player_id,
            "name": player_stats.player.name,
            "goals": player_stats.goals,
            "assists": player_stats.assists,
            "penalty_min": player_stats.penalty_min
    }


@players_router.patch("/players/{player_id}/stats")
def patch_player_stats(
    player_id: int,
    updates: PatchPlayerStats,
    db: Session = Depends(get_db),
):
    stats = db.get(PlayerStats, player_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Stats not found")

    return crud.update_player_stats(db, stats, updates)

