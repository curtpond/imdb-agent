"""Generate embeddings for movie overviews using OpenAI."""

import os
from dotenv import load_dotenv
import openai
import snowflake.connector
from typing import List, Dict
import json

# Load environment variables
load_dotenv()

# Configure OpenAI
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
print(f"Using API key starting with: {api_key[:10]}...")

# Configure Snowflake connection
snowflake_config = {
    'user': os.getenv('SNOWFLAKE_USER'),
    'password': os.getenv('SNOWFLAKE_PASSWORD'),
    'account': os.getenv('SNOWFLAKE_ACCOUNT'),
    'database': 'MOVIES_DB',
    'schema': 'MOVIES_SCHEMA',
    'warehouse': 'COMPUTE_WH'  # Adding default warehouse
}

def get_embedding(text: str) -> List[float]:
    """Get embedding from OpenAI API."""
    client = openai.OpenAI(api_key=api_key)
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def update_movie_embeddings():
    """Update movie embeddings in Snowflake."""
    # Connect to Snowflake
    conn = snowflake.connector.connect(**snowflake_config)
    cursor = conn.cursor()
    
    try:
        # Get movies without embeddings
        cursor.execute("""
            SELECT movie_id, processed_overview 
            FROM movies 
            WHERE overview_embedding IS NULL 
            AND processed_overview IS NOT NULL
        """)
        movies = cursor.fetchall()
        
        print(f"Found {len(movies)} movies without embeddings")
        
        # Process each movie
        for movie_id, overview in movies:
            if not overview:
                continue
                
            # Get embedding
            embedding = get_embedding(overview)
            
            # Convert embedding to JSON array
            cursor.execute("""
                UPDATE movies 
                SET 
                    overview_embedding = PARSE_JSON(%s),
                    updated_at = CURRENT_TIMESTAMP()
                WHERE movie_id = %s
            """, (json.dumps(embedding), movie_id))
            
            print(f"Updated movie {movie_id}")
            
        conn.commit()
        print("Embeddings update completed successfully")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    update_movie_embeddings()
