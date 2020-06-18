from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator


# Default settings for my dag
default_args = {
    'owner': 'hyyyy',
    'start_date': datetime(2020, 6, 1, 0, 0, 0),
    'depends_on_past': False,
    'catchup': False,
    'email_on_failure': True,
    'email_on_retry': False
}

# DAG with schedule interval once an  hour
dag = DAG(
    dag_id='drop_create_tables',
    default_args=default_args,
    description='For dropping and creating tables',
    schedule_interval=None
)

# Dummy operator for beginning
start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

# Drop tables if exists
drop_tables = PostgresOperator(
    task_id='Drop_tables_if_exist',
    dag=dag,
    postgres_conn_id='redshift',
    sql='drop_tables.sql'
)

# Create tables if not exists
create_tables = PostgresOperator(
    task_id='Create_tables_if_not_exist',
    dag=dag,
    postgres_conn_id='redshift',
    sql='create_tables.sql'
)

# Dummy operator for ending
end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

# Dependencies
start_operator >> drop_tables >> create_tables >> end_operator
