from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from plugins.operators import (StageToRedshiftOperator,
                               LoadDimensionOperator,
                               DataQualityOperator)
from plugins.helpers import SqlQueries

# S3 bucket source
IMMIGRATION_DATA = 's3://udacity-hyyyy/capstone/raw_data/sas_data'
TEMPERATURE_DATA = 's3://udacity-hyyyy/capstone/raw_data/GlobalLandTemperaturesByCity.csv'
DEMOGRAPHY_DATA = 's3://udacity-hyyyy/capstone/raw_data/us-cities-demographics.csv'


# Default settings for my dag
default_args = {
    'owner': 'hyyyy',
    'start_date': datetime(2020, 1, 1, 0, 0, 0),
    'depends_on_past': False,
    'catchup': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(hours=1),
    'max_active_runs': 1
}

# DAG with schedule interval once an  hour
dag = DAG(
    dag_id='immigration_etl',
    default_args=default_args,
    description='ETL for immigration data',
    schedule_interval='@yearly'
)

# Dummy operator for beginning
start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

# Load immigration data from S3 to Redshift
stage_immigration_to_redshift = StageToRedshiftOperator(
    task_id='Stage_immigration',
    dag=dag,
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket=IMMIGRATION_DATA,
    table='Staging_Immigration',
    data_format='parquet'
)

# Load demography data from S3 to Redshift
stage_demography_to_redshift = StageToRedshiftOperator(
    task_id='Stage_demography',
    dag=dag,
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket=DEMOGRAPHY_DATA,
    table='Staging_Demography',
    data_format='csv',
    delimiter=';'
)

# Load temperature data from S3 to Redshift
stage_temperature_to_redshift = StageToRedshiftOperator(
    task_id='Stage_temperature',
    dag=dag,
    redshift_conn_id='redshift',
    aws_credentials_id='aws_credentials',
    s3_bucket=TEMPERATURE_DATA,
    table='Staging_Temperature',
    data_format='csv',
    delimiter=','
)

# Insert dimension table dim_demography
insert_demography_table = LoadDimensionOperator(
    task_id='Load_dim_demography_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='dim_demography',
    sql=SqlQueries.dim_demography_insert,
    is_truncate=True
)

# Insert dimension table dim_temperature
insert_temperature_table = LoadDimensionOperator(
    task_id='Load_dim_temperature_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='dim_temperature',
    sql=SqlQueries.dim_temperature_insert,
    is_truncate=True
)

# Insert dimension table dim_date
insert_date_table = LoadDimensionOperator(
    task_id='Load_dim_date_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='dim_date',
    sql=SqlQueries.dim_date_insert,
    is_truncate=True
)

# Insert dimension table dim_immigration
insert_immigration_table = LoadDimensionOperator(
    task_id='Load_dim_immigration_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='dim_immigration',
    sql=SqlQueries.dim_immigration_inset,
    is_truncate=True
)

# Insert fact table fact_immigration_info
insert_fact_table = LoadDimensionOperator(
    task_id='Load_fact_immigration_info_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='fact_immigration_info',
    sql=SqlQueries.fact_immigration_info_insert,
    is_truncate=True
)

# Data Quality Check
table_names = ['dim_temperature', 'dim_demography',
               'dim_immigration', 'dim_date',
               'fact_immigration_info']
quality_check = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id='redshift',
    table_list=table_names,
    expected_result=1,
)

# Dummy operator for ending
end_operator = DummyOperator(task_id='Stop_execution', dag=dag)

# Dependencies
staging_list = [stage_immigration_to_redshift,
                stage_temperature_to_redshift,
                stage_demography_to_redshift]

# S3 to Redshift
start_operator >> staging_list

# Staging tables to dimension and fact tables
staging_list >> insert_temperature_table
staging_list >> insert_demography_table
staging_list >> insert_immigration_table

# Load fact table and then do quality check
insert_temperature_table >> insert_date_table >> insert_fact_table >> quality_check
insert_demography_table >> quality_check
insert_immigration_table >> quality_check

# end of dag
quality_check >> end_operator

