from sqlalchemy import String, Integer, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(12), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)



from typing import Optional, List
from sqlalchemy import (
    Integer, String, Boolean, ForeignKey,
    CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

## Teams table

class Team(Base):
    __tablename__ = "teams"

    team_id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    team_name: Mapped[str] = mapped_column(
        String(64), index=True, nullable=False
    )

    captain_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("draft_players.player_id"),
        nullable=True
    )

    logo_url: Mapped[Optional[str]] = mapped_column(String(200))
    group: Mapped[Optional[str]] = mapped_column(String(1))

    wins: Mapped[int] = mapped_column(default=0)
    draws: Mapped[int] = mapped_column(default=0)
    losses: Mapped[int] = mapped_column(default=0)
    games: Mapped[int] = mapped_column(default=0)
    goals_for: Mapped[int] = mapped_column(default=0)
    goals_against: Mapped[int] = mapped_column(default=0)

    # Relationships
    players: Mapped[List["Player"]] = relationship(
        back_populates="team",
        foreign_keys="Player.team_id",
    )

    captain: Mapped[Optional["Player"]] = relationship(
        foreign_keys=[captain_id],
        post_update=True,  # avoids circular FK issues
    )

    home_matches: Mapped[List["Match"]] = relationship(
        back_populates="home_team",
        foreign_keys="Match.home_team_id",
    )

    away_matches: Mapped[List["Match"]] = relationship(
        back_populates="away_team",
        foreign_keys="Match.away_team_id",
    )

## Players table

class Player(Base):
    __tablename__ = "draft_players"

    ### Constraint to make player + shirt number unique. Use if migrating to Alembic
    # __table_args__ = (
    #     UniqueConstraint("team_id", "shirt_number", name="uq_team_shirt"),
    # )

    player_id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    team_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("teams.team_id"),
        index=True,
        nullable=True
    )

    image_url: Mapped[Optional[str]] = mapped_column(String(200))
    name: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    age: Mapped[int]
    shirt_number: Mapped[int]
    lefthanded: Mapped[bool] = mapped_column(default=False)
    recruiter: Mapped[Optional[str]] = mapped_column(String(16))
    primary_pos: Mapped[Optional[str]] = mapped_column(String(2))
    secondary_pos: Mapped[Optional[str]] = mapped_column(String(2))
    playstyle: Mapped[Optional[str]] = mapped_column(String(64))
    experience: Mapped[int] = mapped_column(default=0)
    licenced: Mapped[bool] = mapped_column(default=False)

    # Relationships
    team: Mapped[Optional[Team]] = relationship(
        back_populates="players",
        foreign_keys=[team_id],
    )

    stats: Mapped[Optional["PlayerStats"]] = relationship(
        back_populates="player",
        uselist=False,
        cascade="all, delete-orphan",
    )

## Stats table 

class PlayerStats(Base):
    __tablename__ = "player_stats"

    player_id: Mapped[int] = mapped_column(
        ForeignKey("draft_players.player_id"),
        primary_key=True
    )

    goals: Mapped[int] = mapped_column(default=0)
    assists: Mapped[int] = mapped_column(default=0)
    played_games: Mapped[int] = mapped_column(default=0)
    penalty_min: Mapped[int] = mapped_column(default=0)

    player: Mapped[Player] = relationship(
        back_populates="stats"
    )

## Matches table

class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        CheckConstraint(
            "home_team_id <> away_team_id",
            name="ck_matches_home_neq_away",
        ),
    )

    match_id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    playoff: Mapped[bool] = mapped_column(default=False, index=True)

    home_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.team_id"),
        index=True,
        nullable=False
    )
    away_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.team_id"),
        index=True,
        nullable=False
    )

    home_score: Mapped[int] = mapped_column(default=0)
    away_score: Mapped[int] = mapped_column(default=0)
    match_time: Mapped[Optional[str]] = mapped_column(String(10)) 
    finished: Mapped[bool] = mapped_column(default="False")

    home_team: Mapped[Team] = relationship(
        back_populates="home_matches",
        foreign_keys=[home_team_id],
    )

    away_team: Mapped[Team] = relationship(
        back_populates="away_matches",
        foreign_keys=[away_team_id],
    )