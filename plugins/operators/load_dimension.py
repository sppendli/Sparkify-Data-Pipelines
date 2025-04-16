from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from helpers import SqlQueries

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self, table, redshift_conn_id, sql_query, append_only=False, *args, **kwargs):
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.sql_query = sql_query
        self.append_only = append_only

    def execute(self, context):
        self.log.info('LoadDimensionOperator not implemented yet')
        redshift_hook = PostgresHook(self.redshift_conn_id)

        if not self.append_only:
            self.log.info(f"Deleting {self.table} table")
            redshift_hook.run(f"DELETE FROM {self.table}")

        self.log.info(f"Data from Fact table => {self.table} table")
        formatted_sql = getattr(SqlQueries, self.sql_query).format(self.table)
        redshift_hook.run(formatted_sql)

        self.log.info(f"Data loaded into {self.table} table")
