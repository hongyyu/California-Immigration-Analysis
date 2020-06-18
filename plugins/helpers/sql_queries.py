class SqlQueries:
    """Process data at Staging tables for further inserting"""
    fact_immigration_info_insert = ("""
        select
            si.cicid as cicid,
            si.admnum as admnum,
            si.count::integer as count,
            si.visatype as visatype,
            si.gender as gender,
            si.occup as occup
        from staging_immigration si
        where i94addr = 'CA'
    """)

    dim_immigration_inset = ("""
        select
            cicid,
            i94yr,
            i94mon,
            i94cit,
            i94res,
            i94port,
            arrdate,
            i94mode,
            i94addr,
            depdate,
            i94bir,
            i94visa,
            dtadfile,
            visapost,
            entdepa,
            entdepd,
            entdepu,
            matflag,
            biryear,
            dtaddto,
            insnum,
            airline,
            fltno
        from staging_immigration
        where i94addr = 'CA'
    """)

    dim_demography_insert = ("""
        select
            city,
            state,
            median_age::Double Precision,
            male_population::integer,
            female_population::integer,
            total_population::integer,
            number_of_veterans::integer,
            foreign_born::integer,
            average_household_size::decimal as avg_household_size,
            state_code,
            race,
            count::integer
        from staging_demography
        where state_code = 'CA'
    """)

    dim_temperature_insert = ("""
        select
            to_date(dt, 'YYYY-MM-DD') as datetime,
            cast(case 
                    when average_temperature='' then '0' 
                    else average_temperature 
                    end as Double Precision) as avg_temperature,
            cast(case 
                    when average_temperature_uncertainty='' then '0' 
                    else average_temperature_uncertainty 
                    end as Double Precision) as avg_temperature_uncer,
            city,
            country,
            latitude,
            longitude
        from staging_temperature
        where country = 'United States'
        and city in (
            select city
            from staging_demography
            where state_code = 'CA'
        )
    """)

    dim_date_insert = ("""
        SELECT 
            distinct dt as datetime, 
            extract(hour from datetime) as hour, 
            extract(day from datetime) as day, 
            extract(week from datetime) as week, 
            extract(month from datetime) as month, 
            extract(year from datetime) as year, 
            extract(dayofweek from datetime) as dayofweek
        FROM dim_temperature
    """)