from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


class Team(BaseModel):
    id: int
    name: str
    short_name: str
    strength: int
    strength_overall_home: int
    strength_overall_away: int
    strength_attack_home: int
    strength_attack_away: int
    strength_defence_home: int
    strength_defence_away: int


class Player(BaseModel):
    id: int
    first_name: str
    second_name: str
    web_name: str
    position: Literal[1, 2, 3, 4] = Field(alias="element_type")
    team_id: int = Field(alias="team_code")
    cost: Annotated[
        float,
        BeforeValidator(lambda x: x / 10),
    ] = Field(alias="now_cost")
    minutes: int
    goals_scored: int
    assists: int
    clean_sheets: int
    goals_conceded: int
    own_goals: int
    penalties_saved: int
    penalties_missed: int
    yellow_cards: int
    red_cards: int
    saves: int
    bonus: int
    bps: int
    influence: float
    creativity: float
    threat: float
    ict_index: float
    starts: int
    now_cost_rank: int
    now_cost_rank_type: int
    form_rank: int
    form_rank_type: int
    points_per_game_rank: int
    points_per_game_rank_type: int
    selected_rank: int
    selected_rank_type: int
    selected_by_percent: float
    total_points: int
    transfers_in: int
    transfers_in_event: int
    transfers_out: int
    transfers_out_event: int
    model_config = ConfigDict(extra="ignore")


class TopElementInfo(BaseModel):
    id: int
    points: int


class ChipPlayed(BaseModel):
    chip_name: Literal["bboost", "3xc", "freehit", "wildcard"]
    num_played: int


class Event(BaseModel):
    id: int
    gameweek: str = Field(alias="name")
    average_fplmanager_score: int | None = Field(alias="average_entry_score")
    highest_fplmanager_score: int | None = Field(alias="highest_score")
    highest_scoring_fplmanager_id: int | None = Field(alias="highest_scoring_entry")
    fplmanagers_count: int = Field(alias="ranked_count")
    data_checked: bool
    event_date: datetime = Field(alias="deadline_time")
    chips_played: list[ChipPlayed] = Field(alias="chip_plays")
    most_selected_player: int = Field(alias="most_selected")
    most_transferred_player_in: int = Field(alias="most_transferred_in")
    top_player_info: TopElementInfo = Field(alias="top_element_info")
    transfers_made: int | None
    most_captained: int | None
    most_vice_captained: int | None


class StatEntry(BaseModel):
    value: int
    element: int


class Stat(BaseModel):
    identifier: str
    a: list[StatEntry] = Field(default_factory=list)
    h: list[StatEntry] = Field(default_factory=list)


class Fixture(BaseModel):
    code: int
    event: int
    finished: bool
    finished_provisional: bool
    id: int
    kickoff_time: datetime
    minutes: int
    provisional_start_time: bool
    started: bool
    team_a: int
    team_a_score: int | None
    team_h: int
    team_h_score: int | None
    stats: list[Stat] = Field(default_factory=list)
    team_h_difficulty: int
    team_a_difficulty: int
    pulse_id: int
