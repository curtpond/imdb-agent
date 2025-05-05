"""IMDB Agent for interacting with Snowflake data."""

from typing import List, Dict, Any
from .snowflake_connector import SnowflakeConnector

class IMDBAgent:
    def __init__(self, snowflake_password: str):
        self.connector = SnowflakeConnector()
        self.connector.connect(snowflake_password)

    def search_movies_by_genre(self, genre: str) -> List[Dict[str, Any]]:
        """Search movies by genre."""
        query = """
        SELECT * FROM movies_by_genre 
        WHERE LOWER(genres) LIKE LOWER(:genre)
        ORDER BY imdb_rating DESC
        LIMIT 5
        """
        results = self.connector.execute_query(query, {'genre': f'%{genre}%'})
        return [dict(zip(['title', 'year', 'rating', 'genres'], row)) for row in results]

    def search_movies_by_actor(self, actor: str) -> List[Dict[str, Any]]:
        """Search movies by actor."""
        query = """
        SELECT * FROM movies_by_actor
        WHERE LOWER(actor) LIKE LOWER(:actor)
        ORDER BY imdb_rating DESC
        """
        results = self.connector.execute_query(query, {'actor': f'%{actor}%'})
        return [dict(zip(['title', 'year', 'rating', 'actor', 'role'], row)) for row in results]

    def get_top_rated_movies(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top rated movies."""
        query = """
        SELECT * FROM top_rated_movies
        ORDER BY imdb_rating DESC
        LIMIT :limit
        """
        results = self.connector.execute_query(query, {'limit': limit})
        return [dict(zip(['title', 'year', 'rating', 'votes', 'genres'], row)) for row in results]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connector.close()
