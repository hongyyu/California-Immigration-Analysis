from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class StageToRedshiftOperator(BaseOperator):
    """Task to copy data from S3 into tables at Redshift cluster

    :param redshift_conn_id: get redshift hook stored at Airflow
    :type redshift_conn_id: String
    :param aws_credentials_id: get AWS ID and secret Key stored at Airflow
    :type aws_credentials_id: String
    :param s3_bucket: data source at AWS S3
    :type s3_bucket: String
    :param table: staging table name for storing primary data source
    :type table: String
    :param json_format: specific json format of data source (either 'auto' or s3 path in this project)
    :type json_format: String
    """
    # Task background color
    ui_color = '#358140'
    # Template for copy SQL task
    copy_csv_sql = """
        COPY {}
        FROM '{}'
        IAM_ROLE '{}'
        delimiter '{}'
        IGNOREHEADER 1
    """
    copy_parquet_sql = """
        COPY {}
        FROM '{}'
        IAM_ROLE '{}'
        FORMAT AS {}
    """

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 aws_credentials_id="",
                 s3_bucket="",
                 table="",
                 data_format="",
                 delimiter="",
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id = aws_credentials_id
        self.s3_bucket = s3_bucket
        self.table = table
        self.data_format = data_format
        self.delimiter = delimiter

    def execute(self, context):
        # Get AWS ID and Key, and hook of Redshift cluster
        self.log.info(f'Start to load and transform {self.table} table')
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)

        # Clearing previous loaded data in the staging table
        self.log.info('Firstly, clearing data from destination Redshift table')
        redshift.run("DELETE FROM {}".format(self.table))

        # Copy data from S3 into staging tables at Redshift cluster
        self.log.info('Copying data from S3 to Redshift')
        if self.data_format == 'csv':
            formatted_sql = StageToRedshiftOperator.copy_csv_sql.format(
                self.table,
                self.s3_bucket,
                credentials.access_key,
                self.delimiter
            )
        elif self.data_format == 'parquet':
            formatted_sql = StageToRedshiftOperator.copy_parquet_sql.format(
                self.table,
                self.s3_bucket,
                credentials.access_key,
                self.data_format
            )
        redshift.run(formatted_sql)
