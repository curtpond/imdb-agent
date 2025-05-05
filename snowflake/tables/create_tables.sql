-- Create a database and schema for the IMDB data
CREATE DATABASE IF NOT EXISTS IMDB_DB;
USE DATABASE IMDB_DB;

CREATE SCHEMA IF NOT EXISTS MOVIES;
USE SCHEMA MOVIES;

-- Create a sequence for movie IDs
CREATE OR REPLACE SEQUENCE movie_id_seq START = 1 INCREMENT = 1;

-- Create the movies table
CREATE OR REPLACE TABLE movies (
    movie_id NUMBER DEFAULT movie_id_seq.NEXTVAL,
    series_title VARCHAR(500) NOT NULL,
    release_year NUMBER(4,0),
    certificate VARCHAR(10),
    runtime_minutes NUMBER(4,0),
    imdb_rating FLOAT,
    meta_score FLOAT,
    num_votes NUMBER(10,0),
    gross_amount NUMBER(12,0),
    processed_overview TEXT,
    overview_embedding VECTOR(1536),  -- For OpenAI embeddings
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    -- Add search optimization for text fields
    SEARCH_OPTIMIZATION = ON,
    -- Add primary key
    CONSTRAINT pk_movies PRIMARY KEY (movie_id),
    -- Add unique constraint on title
    CONSTRAINT uq_movies_title UNIQUE (series_title)
);

-- Create the genres table
CREATE OR REPLACE TABLE genres (
    genre_id NUMBER IDENTITY(1,1),
    movie_id NUMBER NOT NULL,
    genre VARCHAR(50) NOT NULL,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    -- Add primary key
    CONSTRAINT pk_genres PRIMARY KEY (genre_id),
    -- Add foreign key
    CONSTRAINT fk_genres_movie FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    -- Add unique constraint to prevent duplicates
    CONSTRAINT uq_movie_genre UNIQUE (movie_id, genre)
);

-- Create the credits table
CREATE OR REPLACE TABLE credits (
    credit_id NUMBER IDENTITY(1,1),
    movie_id NUMBER NOT NULL,
    person_name VARCHAR(200) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    -- Add primary key
    CONSTRAINT pk_credits PRIMARY KEY (credit_id),
    -- Add foreign key
    CONSTRAINT fk_credits_movie FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    -- Add search optimization for person names
    SEARCH_OPTIMIZATION = ON
);

-- Create the keywords table
CREATE OR REPLACE TABLE keywords (
    keyword_id NUMBER IDENTITY(1,1),
    movie_id NUMBER NOT NULL,
    keyword VARCHAR(100) NOT NULL,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    -- Add primary key
    CONSTRAINT pk_keywords PRIMARY KEY (keyword_id),
    -- Add foreign key
    CONSTRAINT fk_keywords_movie FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    -- Add unique constraint to prevent duplicates
    CONSTRAINT uq_movie_keyword UNIQUE (movie_id, keyword)
);

-- Create indexes for better query performance
CREATE OR REPLACE INDEX idx_movies_release_year ON movies(release_year);
CREATE OR REPLACE INDEX idx_movies_rating ON movies(imdb_rating DESC);
CREATE OR REPLACE INDEX idx_genres_genre ON genres(genre);
CREATE OR REPLACE INDEX idx_credits_person ON credits(person_name);
CREATE OR REPLACE INDEX idx_credits_role ON credits(role);
CREATE OR REPLACE INDEX idx_keywords_keyword ON keywords(keyword);

-- Create a view for movie details with genres
CREATE OR REPLACE VIEW v_movie_details AS
SELECT 
    m.movie_id,
    m.series_title,
    m.release_year,
    m.certificate,
    m.runtime_minutes,
    m.imdb_rating,
    m.meta_score,
    m.processed_overview,
    LISTAGG(DISTINCT g.genre, ', ') WITHIN GROUP (ORDER BY g.genre) as genres,
    ARRAY_AGG(DISTINCT k.keyword) WITHIN GROUP (ORDER BY k.keyword) as keywords
FROM movies m
LEFT JOIN genres g ON m.movie_id = g.movie_id
LEFT JOIN keywords k ON m.movie_id = k.movie_id
GROUP BY 
    m.movie_id,
    m.series_title,
    m.release_year,
    m.certificate,
    m.runtime_minutes,
    m.imdb_rating,
    m.meta_score,
    m.processed_overview;
