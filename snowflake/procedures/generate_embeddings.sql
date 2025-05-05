-- Create a procedure to update embeddings using OpenAI
CREATE OR REPLACE PROCEDURE update_movie_embeddings()
RETURNS STRING
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
BEGIN
    -- Update the overview embeddings using Snowflake's OpenAI integration
    UPDATE movies
    SET 
        overview_embedding = OPENAI_EMBED(processed_overview, 'text-embedding-ada-002'),
        updated_at = CURRENT_TIMESTAMP()
    WHERE overview_embedding IS NULL
    AND processed_overview IS NOT NULL;
    
    RETURN 'Embeddings updated successfully';
END;
$$;

-- Create a similarity search function
CREATE OR REPLACE FUNCTION find_similar_movies(search_text STRING, limit_num INT)
RETURNS TABLE (
    movie_id NUMBER,
    series_title STRING,
    similarity FLOAT,
    processed_overview STRING,
    genres STRING
)
AS
$$
    WITH similarity_scores AS (
        SELECT 
            m.movie_id,
            m.series_title,
            m.processed_overview,
            LISTAGG(DISTINCT g.genre, ', ') WITHIN GROUP (ORDER BY g.genre) as genres,
            VECTOR_COSINE_SIMILARITY(
                m.overview_embedding,
                OPENAI_EMBED(search_text, 'text-embedding-ada-002')
            ) as similarity
        FROM movies m
        LEFT JOIN genres g ON m.movie_id = g.movie_id
        WHERE m.overview_embedding IS NOT NULL
        GROUP BY 1, 2, 3, m.overview_embedding
    )
    SELECT 
        movie_id,
        series_title,
        similarity,
        processed_overview,
        genres
    FROM similarity_scores
    ORDER BY similarity DESC
    LIMIT limit_num
$$;
