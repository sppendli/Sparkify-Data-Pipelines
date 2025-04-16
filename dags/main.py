from datetime import datetime, timedelta
import pendulum
import os
from airflow.decorators import dag
from airflow.operators.dummy import DummyOperator
from operators import (StageToRedshiftOperator, LoadFactOperator,
                       LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

default_args = {
    'owner': 'udacity',
    'start_date': pendulum.now(),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup_by_default': False,
    'email_on_retry': False
}

@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='0 * * * *'
)
def final_project():

    start_operator = DummyOperator(task_id='Begin_execution')

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        table="staging_events",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket="psp-airflow",
        s3_key="log-data",
        file_format="JSON"
        # json_path='s3://psp-airflow/log_json_path.json'
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        table="staging_songs",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket="psp-airflow",
        s3_key="song-data",
        file_format="JSON"
        # json_path='auto'
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        table="songplays",
        redshift_conn_id="redshift",
        sql_query="songplay_table_insert",
        append_only=False
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        table="users",
        redshift_conn_id="redshift",
        sql_query="user_table_insert",
        append_only=False
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id="redshift",
        table="songs",
        sql_query="song_table_insert",
        append_only=False
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        table="artists",
        redshift_conn_id="redshift",
        sql_query="artist_table_insert",
        append_only=False
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        table="time",
        redshift_conn_id="redshift",
        sql_query="time_table_insert",
        append_only=False
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        tables=["songs", "artists", "users", "time"],
        redshift_conn_id="redshift"
    )

    end_operator = DummyOperator(task_id="Stop_execution")

    start_operator >> stage_events_to_redshift >> load_songplays_table
    start_operator >> stage_songs_to_redshift >> load_songplays_table

    load_songplays_table >> load_song_dimension_table >> run_quality_checks
    load_songplays_table >> load_user_dimension_table >> run_quality_checks
    load_songplays_table >> load_artist_dimension_table >> run_quality_checks
    load_songplays_table >> load_time_dimension_table >> run_quality_checks

    run_quality_checks >> end_operator

final_project_dag = final_project()
