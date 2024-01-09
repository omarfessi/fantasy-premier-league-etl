import datetime

import jinja2
import requests
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from operators import CreateTablesOperator

DAG_ID = "fpl_elt"
POSTGRES_CONN_ID = "airflow_pg_cnx"
BOOTSTRAP_STATIC_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M")

template_path = "teams.j2"
rendered_sql = f"rendered_templates/teams/rendered.sql"


def initialize_template_environment(searchpath):
    templateLoader = jinja2.FileSystemLoader(searchpath=searchpath)
    templateEnv = jinja2.Environment(loader=templateLoader)
    return templateEnv


def call_api(bootstrap_static_url):
    payload = {}
    headers = {}
    response = requests.request(
        "GET", bootstrap_static_url, headers=headers, data=payload
    )
    return response


def transform_teams(response):
    teams_json_format = response.json()["teams"]
    data = [
        {"id": team["id"], "name": team["name"], "short_name": team["short_name"]}
        for team in teams_json_format
    ]
    return data


def render_template(**kwargs):
    response = call_api(BOOTSTRAP_STATIC_URL)
    data = transform_teams(response)

    templateEnv = initialize_template_environment(searchpath="templates/INSERTIONS/")
    template = templateEnv.get_template(template_path)
    outputText = template.render(data=data)

    with open(rendered_sql, "w") as output_file:
        output_file.write(outputText)


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
        provide_context=True,  # Pass the context to the PythonOperator
    )
    populate_teams_table = PostgresOperator(
        task_id="populate_teams_table",
        sql="teams/rendered.sql",
        postgres_conn_id=POSTGRES_CONN_ID,
    )

    start_operator >> create_all_tables >> render_template_task >> populate_teams_table
