from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    password: str

    
class LoginRequest(BaseModel):
    username: str
    password: str
    
class ReadMatches(BaseModel):
    match_id: int
    playoff: bool
    home_team_id: int
    away_team_id: int
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