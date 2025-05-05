"""Streamlit interface for the Movie Semantic Agent."""

import os
import streamlit as st
from dotenv import load_dotenv
from agent.src.semantic_agent import MovieSemanticAgent

# Load environment variables
load_dotenv()

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def initialize_agent():
    """Initialize the agent with credentials."""
    return MovieSemanticAgent(
        snowflake_password=os.getenv('SNOWFLAKE_PASSWORD'),
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )

# Page config
st.set_page_config(
    page_title="Movie Recommendation Agent",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Intelligent Movie Recommendation System")

# Sidebar
with st.sidebar:
    st.header("Search Options")
    search_type = st.radio(
        "Choose your search type:",
        ["Semantic Search", "Chat with Agent"]
    )
    
    if search_type == "Semantic Search":
        st.info("""
        Describe the kind of movie you're looking for. For example:
        - A heartwarming story about family relationships
        - An action-packed sci-fi with plot twists
        - A psychological thriller with deep characters
        """)
    else:
        st.info("""
        Ask questions about movies or get recommendations. For example:
        - What are some movies similar to Inception?
        - Suggest movies that combine romance and science fiction
        - What are the best drama movies from the 90s?
        """)

# Main content
if search_type == "Semantic Search":
    query = st.text_area("Describe the type of movie you're looking for:", height=100)
    
    if st.button("Search"):
        with st.spinner("Searching for movies..."):
            with initialize_agent() as agent:
                # Load data if not already loaded
                agent.load_movie_data()
                results = agent.find_similar_movies(query)
                
                # Display results
                for movie in results:
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.subheader(movie['title'])
                            st.write(f"**Genres:** {movie['genres']}")
                            st.write(f"**Year:** {movie['year']}")
                        with col2:
                            st.metric("Rating", f"{movie['rating']:.1f}")
                        st.divider()

else:  # Chat interface
    query = st.text_input("Ask me about movies:", key="chat_input")
    
    if st.button("Send"):
        with st.spinner("Thinking..."):
            with initialize_agent() as agent:
                # Load data if not already loaded
                agent.load_movie_data()
                response = agent.chat_about_movies(
                    query, 
                    st.session_state.chat_history
                )
                
                # Update chat history
                st.session_state.chat_history.append((query, response['answer']))
                
                # Display chat history
                for q, a in st.session_state.chat_history:
                    st.write(f"**You:** {q}")
                    st.write(f"**Agent:** {a}")
                    
                    # If there are movie recommendations, show them
                    if 'movies' in response:
                        st.write("**Related Movies:**")
                        for movie in response['movies']:
                            st.write(f"- {movie['title']} ({movie['year']}) - Rating: {movie['rating']}")
