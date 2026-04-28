from sqlalchemy.orm import Session
from auth import hash_password
from models import User, Match, Team, Player, PlayerStats
from schemas import CreateMatch, PatchMatchScore, PatchTeamStats, PatchPlayerStatsDelta



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

def get_all_matches(db: Session) -> list:
    return db.query(Match).all()

def create_match(db: Session, match: CreateMatch) -> Match:
    db_match = Match(**match.model_dump())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def update_match_score(
    db: Session,
    match: Match,
    updates: PatchMatchScore,
) -> Match:
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(match, field, value)

    db.commit()
    db.refresh(match)
    return match

def delete_match(db: Session, match: Match) -> None:
    db.delete(match)
    db.commit()

def get_all_team_stats(db: Session) -> list:
    return db.query(Team).all()

def update_team_stats(
    db: Session,
    team: Team,
    updates: PatchTeamStats
) -> Team:
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(team, field, value)

    db.commit()
    db.refresh(team)
    return team

def get_players_with_teams(
    db: Session,
    team: int 
):
    return (
        db.query(Player)
        .filter(
            Player.team_id == team
        )
        .join(Team, Player.team_id == Team.team_id)
        .all()
    )

def get_player_stats(
    db: Session,
    player: int
):
    return db.get(PlayerStats, player)


def increment_player_stats(
    db: Session,
    stats: PlayerStats,
    delta: PatchPlayerStatsDelta,
) -> PlayerStats:
    if delta.goals:
        stats.goals += delta.goals

    if delta.assists:
        stats.assists += delta.assists

    if delta.penalty_min:
        stats.penalty_min += delta.penalty_min

    db.commit()
    db.refresh(stats)
    return stats
