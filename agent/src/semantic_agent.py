"""Semantic Search Agent using Snowflake's vector similarity search."""

import os
from typing import List, Dict, Any
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
from .snowflake_connector import SnowflakeConnector

class MovieSemanticAgent:
    def __init__(self, snowflake_password: str, openai_api_key: str):
        self.connector = SnowflakeConnector()
        self.connector.connect(snowflake_password)
        self.chat_model = ChatOpenAI(
            openai_api_key=openai_api_key,
            temperature=0.7
        )
        
    def update_embeddings(self) -> str:
        """Update movie embeddings in Snowflake."""
        query = "CALL update_movie_embeddings()"
        result = self.connector.execute_query(query)
        return result[0][0] if result else "No update result"
    
    def find_similar_movies(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Find movies similar to the query description using Snowflake's vector similarity search."""
        query = f"""
        SELECT * FROM TABLE(find_similar_movies(:query, :limit))
        """
        results = self.connector.execute_query(query, {"query": query, "limit": limit})
        
        return [
            {
                'title': row[1],
                'similarity': row[2],
                'overview': row[3],
                'genres': row[4]
            }
            for row in results
        ]
    
    def chat_about_movies(self, query: str, chat_history: List = None) -> Dict[str, Any]:
        """Have a conversation about movies using similar movies as context."""
        # Get similar movies as context
        similar_movies = self.find_similar_movies(query, limit=3)
        
        # Format context
        context = "Based on these similar movies:\n" + "\n".join(
            f"- {movie['title']} ({movie['genres']})\n  {movie['overview']}"
            for movie in similar_movies
        )
        
        # Format conversation history
        messages = []
        if chat_history:
            for human, ai in chat_history:
                messages.extend([
                    HumanMessage(content=human),
                    AIMessage(content=ai)
                ])
        
        # Add current query with context
        messages.append(HumanMessage(content=f"{context}\n\nUser question: {query}"))
        
        # Get response from ChatGPT
        response = self.chat_model.generate(messages)
        answer = response.generations[0][0].text
        
        return {
            'answer': answer,
            'movies': similar_movies
        }
    
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connector.close()
