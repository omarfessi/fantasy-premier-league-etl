import create_tables_sql
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator


class CreateTablesOperator(BaseOperator):
    ui_color = "#0D70F7"

    def __init__(self, postgres_conn_id="", *args, **kwargs):
        super(CreateTablesOperator, self).__init__(*args, **kwargs)
        self.postgres_conn_id = postgres_conn_id

    def execute(self, context):
        pg = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        for table in create_tables_sql.create_all_tables_statement:
            pg.run(table)
