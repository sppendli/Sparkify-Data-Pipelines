class SqlQueries:
    songplay_table_insert = ("""
        INSERT INTO {}(
            start_time,
            user_id,
            level,
            song_id,
            artist_id,
            session_id,
            location,
            user_agent
        )
        SELECT 
            TIMESTAMP 'epoch' + e.ts/1000 * INTERVAL '1 second' AS start_time,
            e.userId AS user_id,
            e.level,
            s.song_id,
            s.artist_id,
            e.sessionId AS session_id,
            e.location,
            e.userAgent AS user_agent
        FROM staging_events e
        LEFT JOIN staging_songs s ON e.song = s.title AND e.artist = s.artist_name
        WHERE e.page = 'NextSong'
    """)

    user_table_insert = ("""
        INSERT INTO {} (
            user_id,
            first_name,
            last_name,
            gender,
            level
        )
        SELECT DISTINCT
            s.userId AS user_id,
            s.firstName AS first_name,
            s.lastName AS last_name,
            s.gender,
            s.level
        FROM staging_events s
    """)

    song_table_insert = ("""
        INSERT INTO {} (
            song_id,
            title,
            artist_id,
            year,
            duration
        )
        SELECT DISTINCT
            s.song_id,
            s.title,
            s.artist_id,
            s.year,
            s.duration
        FROM staging_songs s
    """)

    artist_table_insert = ("""
        INSERT INTO {} (
            artist_id,
            name,
            location,
            latitude,
            longitude
        )
        SELECT DISTINCT
            s.artist_id,
            s.artist_name AS name,
            s.artist_location AS location,
            s.artist_latitude AS latitude,
            s.artist_longitude AS longitude
        FROM staging_songs s
    """)

    time_table_insert = ("""
        INSERT INTO {} (
            start_time,
            hour,
            day,
            week,
            month,
            year,
            weekday
        )
        WITH temp_time AS (
                         SELECT 
                            TIMESTAMP 'epoch' + (ts/1000 * INTERVAL '1 second') AS ts 
                         FROM staging_events
                        )
        SELECT DISTINCT
            ts AS start_time,
            EXTRACT(hour from ts) AS hour,
            EXTRACT(day from ts) AS day,
            EXTRACT(week from ts) AS week,
            EXTRACT(month from ts) AS month,
            EXTRACT(year from ts) AS year,
            EXTRACT(weekday from ts) AS weekday
        FROM temp_time
    """)