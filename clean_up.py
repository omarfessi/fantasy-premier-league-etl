import psycopg2

try:
    conn = psycopg2.connect("host=127.0.0.1 dbname=fpl user=airflow password=airflow")
except psycopg2.Error as e:
    print("Error: Could not make connection to the Postgres database")
    print(e)
    exit(1)

try:
    cur = conn.cursor()
except psycopg2.Error as e:
    print("Error: Could not get cursor to the Database")
    print(e)
    conn.close()
    exit(1)

conn.set_session(autocommit=True)

try:
    cur.execute("DROP TABLE IF EXISTS public.players_stats;")
    print("Table 'players_stats' dropped successfully.")
except psycopg2.Error as e:
    print("Error: Unable to drop the 'players_stats' table")
    print(e)

try:
    cur.execute("DROP TABLE IF EXISTS public.games_results;")
    print("Table 'games_results' dropped successfully.")
except psycopg2.Error as e:
    print("Error: Unable to drop the 'games_results' table")
    print(e)

try:
    cur.execute("DROP TABLE IF EXISTS public.datetime;")
    print("Table 'datetime' dropped successfully.")
except psycopg2.Error as e:
    print("Error: Unable to drop the 'datetime' table")
    print(e)


try:
    cur.execute("DROP TABLE IF EXISTS public.players;")
    print("Table 'players' dropped successfully.")
except psycopg2.Error as e:
    print("Error: Unable to drop the 'players' table")
    print(e)

try:
    cur.execute("DROP TABLE IF EXISTS public.teams;")
    print("Table 'teams' dropped successfully.")
except psycopg2.Error as e:
    print("Error: Unable to drop the 'teams' table")
    print(e)


conn.close()
