CREATE TABLE IF NOT EXISTS public.Staging_Immigration (
	cicid Double Precision,
    i94yr Double Precision not null,
    i94mon Double Precision not null,
    i94cit Double Precision not null,
    i94res Double Precision not null,
    i94port varchar(256) not null,
    arrdate Double Precision not null,
    i94mode Double Precision,
    i94addr varchar(256),
    depdate Double Precision,
    i94bir Double Precision,
    i94visa Double Precision not null,
    count Double Precision not null,
    dtadfile varchar(256),
    visapost varchar(256),
    occup varchar(256),
    entdepa varchar(256),
    entdepd varchar(256),
    entdepu varchar(256),
    matflag varchar(256),
    biryear Double Precision,
    dtaddto varchar(256),
    gender varchar(256),
    insnum varchar(256),
    airline varchar(256),
    admnum Double Precision not null,
    fltno varchar(256),
    visatype varchar(256) not null
);

CREATE TABLE IF NOT EXISTS public.Staging_Demography (
    city varchar(50) primary key,
    state varchar(50) not null,
    median_age varchar(32) not null,
    male_population varchar(32),
    female_population varchar(32),
    total_population varchar(32) not null,
    number_of_veterans varchar(32),
    foreign_born varchar(32),
    average_household_size varchar(32),
    state_code varchar(32) not null,
    race varchar(256) not null,
    count varchar(32) not null
);

CREATE TABLE IF NOT EXISTS public.Staging_Temperature (
    dt varchar(32) not null,
    average_temperature varchar(32),
    average_temperature_uncertainty varchar(32),
    city varchar(32) primary key,
    country varchar(256) not null,
    latitude varchar(32) not null,
    longitude varchar(32) not null
);

CREATE TABLE IF NOT EXISTS public.dim_demography (
    city varchar(50) primary key,
    state varchar(50) not null,
    median_age Double Precision not null,
    male_population integer,
    female_population integer,
    total_population integer not null,
    number_of_veterans integer,
    foreign_born integer,
    average_household_size decimal,
    state_code varchar(32) not null,
    race varchar(256) not null,
    count integer not null
);

CREATE TABLE IF NOT EXISTS public.dim_temperature (
    dt timestamp not null,
    avg_temperature Double Precision,
    avg_temperature_uncer Double Precision,
    city varchar(32) primary key,
    country varchar(256) not null,
    latitude varchar(32) not null,
    longitude varchar(32) not null
);

CREATE TABLE IF NOT EXISTS public.dim_date (
	start_time timestamp NOT NULL primary key,
	hour int4,
	day int4,
	week int4,
	month int4,
	year int4,
	weekday int4
);

CREATE TABLE IF NOT EXISTS public.fact_immigration_info (
	cicid Double Precision primary key,
	admnum Double Precision not null,
	count integer not null,
	visatype varchar(256) not null,
	gender varchar(256),
	occup varchar(256)
);

CREATE TABLE IF NOT EXISTS public.dim_immigration (
	cicid Double Precision primary key,
    i94yr Double Precision not null,
    i94mon Double Precision not null,
    i94cit Double Precision not null,
    i94res Double Precision not null,
    i94port varchar(256) not null,
    arrdate Double Precision not null,
    i94mode Double Precision,
    i94addr varchar(256),
    depdate Double Precision,
    i94bir Double Precision,
    i94visa Double Precision not null,
    dtadfile varchar(256),
    visapost varchar(256),
    entdepa varchar(256),
    entdepd varchar(256),
    entdepu varchar(256),
    matflag varchar(256),
    biryear Double Precision,
    dtaddto varchar(256),
    insnum varchar(256),
    airline varchar(256),
    fltno varchar(256)
);

