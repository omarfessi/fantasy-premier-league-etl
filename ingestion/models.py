from datetime import datetime
from typing import Annotated, Literal

import pyarrow as pa
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

    @classmethod
    def pyarrow_schema(cls):
        return pa.schema(
            [
                ("id", pa.int32()),
                ("name", pa.string()),
                ("short_name", pa.string()),
                ("strength", pa.int32()),
                ("strength_overall_home", pa.int32()),
                ("strength_overall_away", pa.int32()),
                ("strength_attack_home", pa.int32()),
                ("strength_attack_away", pa.int32()),
                ("strength_defence_home", pa.int32()),
                ("strength_defence_away", pa.int32()),
            ]
        )


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

    @classmethod
    def pyarrow_schema(cls):
        return pa.schema(
            [
                ("id", pa.int32()),
                ("first_name", pa.string()),
                ("second_name", pa.string()),
                ("web_name", pa.string()),
                ("position", pa.int8()),
                ("team_id", pa.int32()),
                ("cost", pa.float32()),
                ("minutes", pa.int32()),
                ("goals_scored", pa.int32()),
                ("assists", pa.int32()),
                ("clean_sheets", pa.int32()),
                ("goals_conceded", pa.int32()),
                ("own_goals", pa.int32()),
                ("penalties_saved", pa.int32()),
                ("penalties_missed", pa.int32()),
                ("yellow_cards", pa.int32()),
                ("red_cards", pa.int32()),
                ("saves", pa.int32()),
                ("bonus", pa.int32()),
                ("bps", pa.int32()),
                ("influence", pa.float32()),
                ("creativity", pa.float32()),
                ("threat", pa.float32()),
                ("ict_index", pa.float32()),
                ("starts", pa.int32()),
                ("now_cost_rank", pa.int32()),
                ("now_cost_rank_type", pa.int32()),
                ("form_rank", pa.int32()),
                ("form_rank_type", pa.int32()),
                ("points_per_game_rank", pa.int32()),
                ("points_per_game_rank_type", pa.int32()),
                ("selected_rank", pa.int32()),
                ("selected_rank_type", pa.int32()),
                ("selected_by_percent", pa.float32()),
                ("total_points", pa.int32()),
                ("transfers_in", pa.int32()),
                ("transfers_in_event", pa.int32()),
                ("transfers_out", pa.int32()),
                ("transfers_out_event", pa.int32()),
            ]
        )


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

    @classmethod
    def pyarrow_schema(cls):
        return pa.schema(
            [
                ("id", pa.int32()),
                ("gameweek", pa.string()),
                ("average_fplmanager_score", pa.int32()),
                ("highest_fplmanager_score", pa.int32()),
                ("highest_scoring_fplmanager_id", pa.int32()),
                ("fplmanagers_count", pa.int32()),
                ("data_checked", pa.bool_()),
                ("event_date", pa.timestamp("s")),
                (
                    "chips_played",
                    pa.list_(
                        pa.struct(
                            [
                                ("chip_name", pa.string()),
                                ("num_played", pa.int32()),
                            ]
                        )
                    ),
                ),
                ("most_selected_player", pa.int32()),
                ("most_transferred_player_in", pa.int32()),
                (
                    "top_player_info",
                    pa.struct(
                        [
                            ("id", pa.int32()),
                            ("points", pa.int32()),
                        ]
                    ),
                ),
                ("transfers_made", pa.int32()),
                ("most_captained", pa.int32()),
                ("most_vice_captained", pa.int32()),
            ]
        )


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

    @classmethod
    def pyarrow_schema(cls):
        return pa.schema(
            [
                ("code", pa.int32()),
                ("event", pa.int32()),
                ("finished", pa.bool_()),
                ("finished_provisional", pa.bool_()),
                ("id", pa.int32()),
                ("kickoff_time", pa.timestamp("ms")),
                ("minutes", pa.int32()),
                ("provisional_start_time", pa.bool_()),
                ("started", pa.bool_()),
                ("team_a", pa.int32()),
                ("team_a_score", pa.int32()),
                ("team_h", pa.int32()),
                ("team_h_score", pa.int32()),
                (
                    "stats",
                    pa.list_(
                        pa.struct(
                            [
                                ("identifier", pa.string()),
                                (
                                    "a",
                                    pa.list_(
                                        pa.struct(
                                            [
                                                ("value", pa.int32()),
                                                ("element", pa.int32()),
                                            ]
                                        )
                                    ),
                                ),
                                (
                                    "h",
                                    pa.list_(
                                        pa.struct(
                                            [
                                                ("value", pa.int32()),
                                                ("element", pa.int32()),
                                            ]
                                        )
                                    ),
                                ),
                            ]
                        )
                    ),
                ),
                ("team_h_difficulty", pa.int32()),
                ("team_a_difficulty", pa.int32()),
                ("pulse_id", pa.int32()),
            ]
        )


ModelUnion = Event | Team | Player | Fixture
