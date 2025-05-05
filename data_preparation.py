import pandas as pd
import numpy as np
from datetime import datetime
import re

def clean_runtime(runtime):
    """Extract minutes from runtime string."""
    if pd.isna(runtime):
        return None
    minutes = re.findall(r'(\d+)', str(runtime))
    return int(minutes[0]) if minutes else None

def clean_year(year):
    """Convert year to integer."""
    try:
        return int(year)
    except (ValueError, TypeError):
        return None

def clean_gross(gross):
    """Convert gross amount to numeric value."""
    if pd.isna(gross):
        return None
    # Remove commas and dollar signs
    clean = re.sub(r'[,$]', '', str(gross))
    try:
        return int(clean)
    except ValueError:
        return None

def split_genres(genre):
    """Split genre string into list."""
    if pd.isna(genre):
        return []
    return [g.strip() for g in genre.split(',')]

def prepare_data_for_snowflake(df):
    """
    Prepare IMDB data for Snowflake ingestion and AI agent use.
    Returns multiple dataframes for different tables.
    """
    # Create a copy to avoid modifying original
    df = df.copy()
    
    # Clean and transform data
    df['runtime_minutes'] = df['Runtime'].apply(clean_runtime)
    df['release_year'] = df['Released_Year'].apply(clean_year)
    df['gross_amount'] = df['Gross'].apply(clean_gross)
    df['genres'] = df['Genre'].apply(split_genres)
    
    # Create normalized tables
    
    # 1. Movies table (main table)
    movies_df = df[[
        'Series_Title', 'release_year', 'Certificate', 
        'runtime_minutes', 'IMDB_Rating', 'Meta_score',
        'No_of_Votes', 'gross_amount', 'processed_overview'
    ]].copy()
    movies_df['movie_id'] = range(1, len(movies_df) + 1)
    
    # 2. Genres table (normalized from the genres list)
    genres_data = []
    for movie_id, genres in enumerate(df['genres'], 1):
        for genre in genres:
            genres_data.append({
                'movie_id': movie_id,
                'genre': genre
            })
    genres_df = pd.DataFrame(genres_data)
    
    # 3. Credits table (normalized from director and stars)
    credits_data = []
    for idx, row in df.iterrows():
        movie_id = idx + 1
        # Add director
        credits_data.append({
            'movie_id': movie_id,
            'person_name': row['Director'],
            'role': 'Director'
        })
        # Add stars
        for i in range(1, 5):
            star = row[f'Star{i}']
            if not pd.isna(star):
                credits_data.append({
                    'movie_id': movie_id,
                    'person_name': star,
                    'role': f'Star{i}'
                })
    credits_df = pd.DataFrame(credits_data)
    
    # 4. Keywords table (from extracted keywords)
    keywords_data = []
    for movie_id, keywords in enumerate(df['keywords'], 1):
        for keyword in keywords:
            keywords_data.append({
                'movie_id': movie_id,
                'keyword': keyword
            })
    keywords_df = pd.DataFrame(keywords_data)
    
    # Add metadata
    current_timestamp = datetime.now().isoformat()
    for df in [movies_df, genres_df, credits_df, keywords_df]:
        df['created_at'] = current_timestamp
        df['updated_at'] = current_timestamp
    
    return {
        'movies': movies_df,
        'genres': genres_df,
        'credits': credits_df,
        'keywords': keywords_df
    }

def save_for_snowflake(dataframes, output_dir):
    """Save prepared dataframes as CSV files for Snowflake ingestion."""
    for name, df in dataframes.items():
        output_path = f"{output_dir}/{name}.csv"
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"Saved {name} to {output_path}")
