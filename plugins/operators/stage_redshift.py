from airflow.secrets.metastore import MetastoreBackend
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'

    @apply_defaults
    def __init__(self, table, redshift_conn_id, aws_credentials_id, s3_bucket, s3_key, file_format, json_path='auto', *args, **kwargs):
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.file_format = file_format
        self.json_path = json_path

    def execute(self, context):
        self.log.info('StageToRedshiftOperator not implemented yet')
        metastoreBackend = MetastoreBackend()
        aws_conn = metastoreBackend.get_connection(self.aws_credentials_id)
        redshift_hook = PostgresHook(self.redshift_conn_id)

        self.log.info("Deleting data in the existing Redshift Table")
        redshift_hook.run(f"DELETE FROM {self.table}")

        self.log.info("Copying data from S3 to Redshift")
        rendered_key = self.s3_key.format(**context)
        s3_path = f"s3://{self.s3_bucket}/{rendered_key}"

        formatted_sql = f"""
            COPY {self.table}
            FROM '{s3_path}'
            ACCESS_KEY_ID '{aws_conn.login}'
            SECRET_ACCESS_KEY '{aws_conn.password}'
            {self.file_format} '{self.json_path}';
        """
        redshift_hook.run(formatted_sql)
        






