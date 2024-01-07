teams_table = """
CREATE table IF NOT exists public.teams(
   id INTEGER,
   name VARCHAR NOT NULL ,
   short_name VARCHAR NOT NULL ,
   PRIMARY KEY(id)
);"""


create_all_tables_statement = [teams_table]
