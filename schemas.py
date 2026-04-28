from pydantic import BaseModel
from typing import Optional

class CreateUser(BaseModel):
    username: str
    password: str

    
class LoginRequest(BaseModel):
    username: str
    password: str

class TeamRead(BaseModel):
    team_id: int
    team_name: str

    class Config:
        from_attributes = True

class ReadMatches(BaseModel):
    match_id: int
    playoff: bool
    home_team: TeamRead
    away_team: TeamRead 
    home_score: int
    away_score: int
    match_time: str
    finished: bool

class CreateMatch(BaseModel):
    playoff: bool
    home_team_id: int
    away_team_id: int
    home_score: int = 0
    away_score: int = 0
    match_time: str
    finished: bool = False

class PatchMatchScore(BaseModel):
    home_score: Optional[int]
    away_score: Optional[int]
    finished: Optional[bool]

class ReadTeamStats(BaseModel):
    team_id: int
    team_name: str
    group: Optional[str]
    wins: int
    draws: int
    losses: int
    games: int
    goals_for: int
    goals_against: int

class PatchTeamStats(BaseModel):
    wins: int
    draws: int
    losses: int
    games: int
    goals_for: int
    goals_against: int

class ReadPlayerTeamInfo(BaseModel):
    player_id: int
    name: str
    shirt_number: int
    team_name: str

    class Config:
        from_attributes = True

class ReadPlayerStats(BaseModel):
    player_id: int
    name: str
    goals: int
    assists: int
    penalty_min: int

    class Config:
        from_attributes = True

class PatchPlayerStatsDelta(BaseModel):
    goals: Optional[int] = 0
    assists: Optional[int] = 0
    penalty_min: Optional[int] = 0
