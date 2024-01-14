datetime_table = """
CREATE TABLE IF NOT EXISTS public.datetime(
   dt_as_timestamp timestamp PRIMARY KEY,
   hour int,
   day int ,
   week int,
   month int,
   year int,
   dayofweek int
);"""

teams_table = """
CREATE table IF NOT exists public.teams(
   id INTEGER,
   name VARCHAR NOT NULL,
   short_name VARCHAR NOT NULL, 
   PRIMARY KEY(id)
);"""

players_table = """
CREATE table IF NOT exists public.players(
   id INTEGER,
   first_name VARCHAR NOT NULL ,
   second_name VARCHAR NOT NULL ,
   web_name VARCHAR NOT NULL,
   position INTEGER NOT NULL,
   team_id INTEGER,
   PRIMARY KEY(id),
   CONSTRAINT fk_teams
      FOREIGN KEY(team_id) 
	      REFERENCES teams(id)
);"""

games_results = """
CREATE table IF NOT exists public.games_results(
   id INTEGER,
   team_h INTEGER REFERENCES teams (id),
   team_a INTEGER REFERENCES teams (id),
   kickoff_time timestamp NOT NULL REFERENCES datetime(dt_as_timestamp),
   team_h_score INTEGER NOT NULL,
   team_a_score INTEGER NOT NULL,
   PRIMARY KEY(id)
);"""

players_stats = """
CREATE table IF NOT exists public.players_stats(
   id SERIAL PRIMARY key,
   game_id INTEGER REFERENCES games_results (id),
   player_id INTEGER NOT null REFERENCES players (id),
   stat_identifier VARCHAR(25) NOT NULL,
   stat_value INTEGER NOT null
);"""


create_all_tables_statement = [
    datetime_table,
    teams_table,
    players_table,
    games_results,
    players_stats,
]
