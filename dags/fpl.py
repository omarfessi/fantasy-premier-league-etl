import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from operators import CreateTablesOperator

# my custom python modules
from tasks.task import render_template

DAG_ID = "fpl_elt"
POSTGRES_CONN_ID = "airflow_pg_cnx"

with DAG(
    dag_id=DAG_ID,
    description="Main DAG for Fantasy Premier League ELT",
    start_date=datetime.datetime(2022, 1, 5),
    schedule_interval="0 0 1 * *",
    catchup=False,
    template_searchpath=["rendered_templates"],
) as dag:
    start_operator = DummyOperator(task_id="begin_execution")
    create_all_tables = CreateTablesOperator(
        task_id="create_all_tables", postgres_conn_id=POSTGRES_CONN_ID, dag=dag
    )
    render_datetime_template_task = PythonOperator(
        task_id="render_template_for_datetime",
        python_callable=render_template,
        op_kwargs={
            "searchpath": "templates",
            "template_path": "datetime.j2",
            "rendered_sql": "rendered_templates/datetime/rendered.sql",
            "transformation_entity": "datetime",
        },
        provide_context=True,
    )

    render_teams_template_task = PythonOperator(
        task_id="render_template_for_teams",
        python_callable=render_template,
        op_kwargs={
            "searchpath": "templates",
            "template_path": "teams.j2",
            "rendered_sql": "rendered_templates/teams/rendered.sql",
            "transformation_entity": "teams",
        },
        provide_context=True,
    )
    render_players_template_task = PythonOperator(
        task_id="render_template_for_players",
        python_callable=render_template,
        op_kwargs={
            "searchpath": "templates",
            "template_path": "players.j2",
            "rendered_sql": "rendered_templates/players/rendered.sql",
            "transformation_entity": "players",
        },
        provide_context=True,
    )

    render_games_results_template_task = PythonOperator(
        task_id="render_template_for_games_results",
        python_callable=render_template,
        op_kwargs={
            "searchpath": "templates",
            "template_path": "games_results.j2",
            "rendered_sql": "rendered_templates/games_results/rendered.sql",
            "transformation_entity": "games_results",
        },
        provide_context=True,
    )
    populate_datetime_table = PostgresOperator(
        task_id="populate_datetime_table",
        sql="datetime/rendered.sql",
        postgres_conn_id=POSTGRES_CONN_ID,
    )

    populate_teams_table = PostgresOperator(
        task_id="populate_teams_table",
        sql="teams/rendered.sql",
        postgres_conn_id=POSTGRES_CONN_ID,
    )

    populate_players_table = PostgresOperator(
        task_id="populate_players_table",
        sql="players/rendered.sql",
        postgres_conn_id=POSTGRES_CONN_ID,
    )

    populate_games_results_table = PostgresOperator(
        task_id="populate_games_results_table",
        sql="games_results/rendered.sql",
        postgres_conn_id=POSTGRES_CONN_ID,
    )

    (
        start_operator
        >> create_all_tables
        >> render_datetime_template_task
        >> render_teams_template_task
        >> render_players_template_task
        >> render_games_results_template_task
        >> populate_datetime_table
        >> populate_teams_table
        >> populate_players_table
        >> populate_games_results_table
    )
