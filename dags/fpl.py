import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from operators import CreateTablesOperator

DAG_ID = "fpl_elt"
POSTGRES_CONN_ID = "airflow_pg_cnx"

with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2022, 1, 5),
    schedule_interval="0 0 1 * *",
    catchup=False,
    template_searchpath=["rendered_templates"],
) as dag:
    start_operator = DummyOperator(task_id="begin_execution")
    create_all_tables = CreateTablesOperator(
        task_id="create_all_tables", postgres_conn_id=POSTGRES_CONN_ID, dag=dag
    )
    populate_teams_table = PostgresOperator(
        task_id="populate_teams_table",
        sql="teams/renderered_sql_20240106_1742.sql",
        postgres_conn_id=POSTGRES_CONN_ID,
    )

    start_operator >> create_all_tables >> populate_teams_table
