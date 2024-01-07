import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

DAG_ID = "fpl_elt"

with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2022, 1, 5),
    schedule_interval="0 0 1 * *",
    catchup=False,
    template_searchpath=["templates/CREATIONS", "rendered_templates"],
) as dag:
    create_teams_table = PostgresOperator(
        task_id="create_teams_table",
        sql="teams.sql",
        postgres_conn_id="airflow_pg_cnx",
    )
    populate_teams_table = PostgresOperator(
        task_id="populate_teams_table",
        sql="teams/renderered_sql_20240106_1742.sql",
        postgres_conn_id="airflow_pg_cnx",
    )

    create_teams_table >> populate_teams_table