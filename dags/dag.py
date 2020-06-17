from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
# from plugins.operators import (StageToRedshiftOperator, LoadFactOperator,
#                                LoadDimensionOperator, DataQualityOperator)
# from plugins.helpers import SqlQueries

# S3 bucket source
IMMIGRATION_DATA = ''
AIRPORT_DATA = ''
TEMPERATURE_DATA = ''
DEMOGRAPHY_DATA = ''

# Default settings for my dag
default_args = {
    'owner': 'hyyyy',
    'start_date': datetime(2020, 1, 1, 0, 0, 0),
    'depends_on_past': False,
    'catchup': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(hours=1),
    'max_active_runs': 1
}

# DAG with schedule interval once an  hour
dag = DAG(
    dag_id='immigration_etl',
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='@yearly'
)

# Dummy operator for beginning
start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)


