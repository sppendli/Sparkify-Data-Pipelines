DROP table IF EXISTS public.artists;

DROP table IF EXISTS public.songplays;

DROP table IF EXISTS public.songs;

DROP table IF EXISTS public.staging_events;

DROP table IF EXISTS public.staging_songs;

DROP table IF EXISTS public."time";

DROP table IF EXISTS public.users;

CREATE TABLE public.artists (
	artist_id varchar(256) NOT NULL,
	name varchar(512),
	location varchar(512),
	latitude numeric(18,0),
	longitude numeric(18,0)
);

CREATE TABLE public.songplays (
	play_id int identity(0,1),
	start_time timestamp NOT NULL,
	user_id varchar(256) NOT NULL,
	"level" varchar(256),
	song_id varchar(256),
	artist_id varchar(256),
	session_id int4,
	location varchar(256),
	user_agent varchar(256),
	CONSTRAINT songplays_pkey PRIMARY KEY (play_id)
);

CREATE TABLE public.songs (
	song_id varchar(256) NOT NULL,
	title varchar(512),
	artist_id varchar(256),
	"year" int4,
	duration numeric(18,0),
	CONSTRAINT songs_pkey PRIMARY KEY (song_id)
);

CREATE TABLE staging_events (
    artist varchar(256),
    auth varchar(256),
    firstName varchar(256),
    gender varchar(1),
    itemInSession int,
    lastName varchar(256),
    length float,
    level varchar(256),
    location varchar(256),
    method varchar(256),
    page varchar(256),
    registration float,
    sessionId int,
    song varchar(256),
    status int,
    ts bigint,
    userAgent varchar(256),
    userId varchar(256)
)

CREATE TABLE staging_songs (
	num_songs int4,
	artist_id varchar(256),
	artist_name varchar(512),
	artist_latitude numeric(18,0),
	artist_longitude numeric(18,0),
	artist_location varchar(512),
	song_id varchar(256),
	title varchar(512),
	duration numeric(18,0),
	"year" int4
)

CREATE TABLE public."time" (
	start_time timestamp NOT NULL,
	"hour" int4,
	"day" int4,
	week int4,
	"month" varchar(256),
	"year" int4,
	weekday varchar(256),
	CONSTRAINT time_pkey PRIMARY KEY (start_time)
) ;

CREATE TABLE public.users (
	user_id int4 NOT NULL,
	first_name varchar(256),
	last_name varchar(256),
	gender varchar(256),
	"level" varchar(256),
	CONSTRAINT users_pkey PRIMARY KEY (user_id)
);
