from datetime import UTC, datetime

import pytest

from cloud_run_ingestion.ingestion.models import Fixture, Stat, StatEntry


@pytest.fixture
def validated_fixtures():
    return [
        Fixture(
            code=2444470,
            event=1,
            finished=True,
            finished_provisional=True,
            id=1,
            kickoff_time=datetime(2024, 8, 16, 19, 0, tzinfo=UTC),
            minutes=90,
            provisional_start_time=False,
            started=True,
            team_a=9,
            team_a_score=0,
            team_h=14,
            team_h_score=1,
            stats=[
                Stat(
                    identifier="goals_scored", a=[], h=[StatEntry(value=1, element=389)]
                ),
                Stat(identifier="assists", a=[], h=[StatEntry(value=1, element=372)]),
            ],
            team_h_difficulty=3,
            team_a_difficulty=3,
            pulse_id=115827,
        ),
        Fixture(
            code=2444473,
            event=1,
            finished=True,
            finished_provisional=True,
            id=4,
            kickoff_time=datetime(2024, 8, 17, 11, 30, tzinfo=UTC),
            minutes=90,
            provisional_start_time=False,
            started=True,
            team_a=12,
            team_a_score=2,
            team_h=10,
            team_h_score=0,
            stats=[
                Stat(
                    identifier="goals_scored",
                    a=[
                        StatEntry(value=1, element=317),
                        StatEntry(value=1, element=328),
                    ],
                    h=[],
                ),
                Stat(
                    identifier="assists",
                    a=[
                        StatEntry(value=1, element=328),
                        StatEntry(value=1, element=336),
                    ],
                    h=[],
                ),
            ],
            team_h_difficulty=5,
            team_a_difficulty=2,
            pulse_id=115830,
        ),
    ]


@pytest.fixture
def valid_fixtures_raw_data():
    return [
        {
            "code": 2444470,
            "event": 1,
            "finished": True,
            "finished_provisional": True,
            "id": 1,
            "kickoff_time": "2024-08-16T19:00:00Z",
            "minutes": 90,
            "provisional_start_time": False,
            "started": True,
            "team_a": 9,
            "team_a_score": 0,
            "team_h": 14,
            "team_h_score": 1,
            "stats": [
                {
                    "identifier": "goals_scored",
                    "a": [],
                    "h": [{"value": 1, "element": 389}],
                },
                {"identifier": "assists", "a": [], "h": [{"value": 1, "element": 372}]},
                {"identifier": "own_goals", "a": [], "h": []},
            ],
            "team_h_difficulty": 3,
            "team_a_difficulty": 3,
            "pulse_id": 115827,
        },
        {
            "code": 2444473,
            "event": 1,
            "finished": True,
            "finished_provisional": True,
            "id": 4,
            "kickoff_time": "2024-08-17T11:30:00Z",
            "minutes": 90,
            "provisional_start_time": False,
            "started": True,
            "team_a": 12,
            "team_a_score": 2,
            "team_h": 10,
            "team_h_score": 0,
            "stats": [
                {
                    "identifier": "goals_scored",
                    "a": [],
                    "h": [{"value": 1, "element": 389}],
                },
                {"identifier": "assists", "a": [], "h": [{"value": 1, "element": 372}]},
                {"identifier": "own_goals", "a": [], "h": []},
            ],
            "team_h_difficulty": 5,
            "team_a_difficulty": 2,
            "pulse_id": 115830,
        },
    ]


@pytest.fixture
def invalid_fixtures_raw_data():
    return [
        {
            # Missing code key
            "event": 1,
            "finished": True,
            "finished_provisional": True,
            "id": 1,
            "kickoff_time": "2024-08-16T19:00:00Z",
            "minutes": 90,
            "provisional_start_time": False,
            "started": True,
            "team_a": 9,
            "team_a_score": 0,
            "team_h": 14,
            "team_h_score": 1,
            "stats": [],
            "team_h_difficulty": 3,
            "team_a_difficulty": 3,
            "pulse_id": 115827,
        },
        {
            "code": 2444473,
            "event": 1,
            "finished": True,
            "finished_provisional": True,
            "id": 4,
            "kickoff_time": "2024-08-17T11:30:00Z",
            "minutes": 90,
            "provisional_start_time": False,
            "started": True,
            "team_a": 12,
            "team_a_score": 2,
            #'team_h' key is missing
            "team_h_score": 0,
            "stats": [
                {
                    "identifier": "goals_scored",
                    "a": [],
                    "h": [{"value": 1, "element": 389}],
                },
                {"identifier": "assists", "a": [], "h": [{"value": 1, "element": 372}]},
                {"identifier": "own_goals", "a": [], "h": []},
            ],
            "team_h_difficulty": 5,
            "team_a_difficulty": 2,
            "pulse_id": 115830,
        },
    ]
