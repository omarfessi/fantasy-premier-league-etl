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
    render_template_task = PythonOperator(
        task_id="render_template",
        python_callable=render_template,
        op_kwargs={
            "searchpath": "templates/INSERTIONS",
            "template_path": "teams.j2",
            "rendered_sql": "rendered_templates/teams/rendered.sql",
        },
        provide_context=True,
    )
    populate_teams_table = PostgresOperator(
        task_id="populate_teams_table",
        sql="teams/rendered.sql",
        postgres_conn_id=POSTGRES_CONN_ID,
    )

    start_operator >> create_all_tables >> render_template_task >> populate_teams_table
