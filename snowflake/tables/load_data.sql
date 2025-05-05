-- Set up file format for CSV loading
CREATE OR REPLACE FILE FORMAT csv_format
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('NULL', 'null')
    EMPTY_FIELD_AS_NULL = TRUE;

-- Create stages for data loading
CREATE OR REPLACE STAGE imdb_movies_stage
    FILE_FORMAT = csv_format;

CREATE OR REPLACE STAGE imdb_genres_stage
    FILE_FORMAT = csv_format;

CREATE OR REPLACE STAGE imdb_credits_stage
    FILE_FORMAT = csv_format;

CREATE OR REPLACE STAGE imdb_keywords_stage
    FILE_FORMAT = csv_format;

-- Load data into tables
COPY INTO movies (
    series_title,
    release_year,
    certificate,
    runtime_minutes,
    imdb_rating,
    meta_score,
    num_votes,
    gross_amount,
    processed_overview,
    created_at,
    updated_at
)
FROM @imdb_movies_stage/movies.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';

COPY INTO genres (
    movie_id,
    genre,
    created_at,
    updated_at
)
FROM @imdb_genres_stage/genres.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';

COPY INTO credits (
    movie_id,
    person_name,
    role,
    created_at,
    updated_at
)
FROM @imdb_credits_stage/credits.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';

COPY INTO keywords (
    movie_id,
    keyword,
    created_at,
    updated_at
)
FROM @imdb_keywords_stage/keywords.csv
FILE_FORMAT = csv_format
ON_ERROR = 'CONTINUE';
