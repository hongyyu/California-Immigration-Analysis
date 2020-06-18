## Summary
The purpose of this project is to build an `auto-pipeline` to generate appropriate 
`Data Warehouse` on the `AWS` for immigration data. Nowadays, more and more people 
are considering to immigrate to other countries for many reasons, including but not 
limit to escape conflict, seek suprior healthcare, education purpose, and etc. Thus, it 
is meaningful to analyze and understand what jobs those immigrants did before immigration, 
where they used to live, and how they arrive the countries. There are many more questions 
we could figure out by utlizing those immigration related dataset. Since the data provided 
here is specific used for the United State, we would focus on analyzing immigrants at 
`California` state.

The purpose of this `data warehoue` is to answer questions like:
1. At california, how many immigrants in the recent years?
2. At which cities in the california, there are more immigrants?
3. Could that possible temperature influence where those immigrants stay?

## Database Schema
Creating and designing the database with star schema. There are 5 tables in total (one fact
table and four dimension tables) showing below with column names in the second line:
#### *Fact Table*
   > fact_immigration_info
   > - cicid, admnum, count, visatype, gender, occup
#### *Dimension Tables*
Some column names in the `dim_immigration` table could be confused, please go to the file
`I94_SAS_Labels_Descriptions.SAS` for more reference.
   > dim_date
   > - datetime, hour, day, week, month, year, weekday

   > dim_immigration
   > - cicid, i94yr, i94mon, i94cit, i94res, i94port, arrdate, i94mode, i94addr, depdate, i94bir,
   > i94visa, dtadfile, visapost, entdepa, entdepd, entdepu, matflag, biryear, dtaddto, insnum,
   > airline, fltno

   > dim_temperature
   > - datetime, avg_temprature, avg_temprature_uncer, city, country, latitude, longitude

   > dim_demography
   > - city, state, median_age, male_population, female_population, total_population, number_of_veterans,
   > foreign_born, avg_household_size, state_code, race, count

## DAG (Directed Acyclic Graph)
Directed Acyclic Graph is a finite direct graph without directed cycles, and we should use a DAG to 
design our data pipeline. There are totally two dags in this project. 

First dag used for dropping and creating tables in the Redshift cluster. It should be run
if there are not tables in your redshift yet so that the schedule intervel is `None`.


![drop_create](/imgs/drop_create.png)

Second dag used for processing and loading data from staging tables into dimension and 
fact table at Redshift cluster. Setting the schedule interval to be `@yearly` or `@monthly`
depending on data source releasing.

![drop_create](/imgs/etl.png)

The steps are as follows:
1. **Drop and Create** all necessary tables at Redshift cluster if exists
2. **Load** data from S3 into staging tables at Redshift
3. **Load** data from staging tables into fact and dimension tables
4. **Check** data quality of all fact and dimension tables

## Choice of Technologies
`Airflow` was chosen because it is easy to monitor and schedule any data pipelines which should
be run on time. We could also share these pipelines with other team members or colleagues as long
as the dag you built are straightforward. Moreover, airflow could run in parallel which make works
more efficient and have easy customize operators for more purposes. Also, by checking the airflow UI,
people could look steps and log at each step in the pipeline for debugging and re-design the pipeline.

`AWS Redshift` is used for maintaining our data warehouse on the cloud. The advantages of choosing
Redshift is obvious because it could provide a scalable system even if we have a lot amount
of data. Meanwhile, getting our data source form S3 which is more compatible to redshift as they
are both one of Amazon Web Service. 

## How to Run
Instead of run Airflow in the local environment, it is easier to run with `docker` container. For installing 
docker, please click [here](https://docs.docker.com/docker-for-mac/install/). 
#### *Set up Docker container*
In order to set up and run Airflow using docker, after instlling docker in your local computer, 
there are several steps:

First, pull and download image to local 
```$xslt
docker pull puckel/docker-airflow
```
Then, run the docker image for Apache Airflow, and now you could visit Airflow UI at 
[http://localhost:8080/](http://localhost:8080/). For make your local project work in the docker container,
set appropriate path `/path/to/your/dag` below.
<pre>
docker run -d -p 8080:8080 -v <b>/path/to/your/dag</b>:/usr/local/airflow/dags  puckel/docker-airflow webserver
</pre>
It is also possible to use command line.
```$xslt
docker exec -ti <container name> bash
```
#### *Set up Connection to **AWS** and **Redshift***
On the Airflow UI, follow the tab Admin -> Connections -> Create to set proper connection to both `AWS` and 
`Redshift`.
- `AWS`
    - Conn Id: aws_credentials
    - Conn Type: Amazon Web Services
    - Login: **Your IAM Role**
- `Redshift`
    - Conn Id: redshift
    - Conn Type: Postgres
    - Host: **Your Redshift Cluster Endpoint**
    - Schema: **Database Name**
    - Login: **Redshift User Name**
    - Password: **Redshift User Password**
    - Port: **Redshift Port**
#### *Run the DAG*
![ui](/imgs/airflow_ui.png)

1. `Open` the Airflow UI
2. There are two dags called `drop_create_tables` and `immigration_etl`. Before running
the ETL pipeline, you should `turn on` and `trigger` the drop_create_tables for the first 
time. 
3. Click `Trigger DAG` for immigration_etl and then wait until complete.

## More Concerns
* If the size of data increased by 100x, which we have already considered the solution by 
expanding our redshift cluster nodes and storage. The drawback is a higher cost.
* The data populates a dashboard that must be updated on a daily basis by 7am every day. Under
this situation, we use airflow to schedule when and what our pipeline need to be run.
* If the database needed to be accessed by 100+ people, we could give them access permissions
to this redshift cluster, and redshift are fully capable to handle this number of visits.
If not, we could simply scale up the size of our cluster.

