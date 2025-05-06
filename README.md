# IMDB Agent: Semantic Movie Search and Recommendations

## Project Overview

This project demonstrates an intelligent movie recommendation system that combines the power of Snowflake for data storage and vector similarity search, LangChain for semantic retrieval, and Streamlit for an interactive user interface. It serves as a proof of concept for building AI-powered agents on top of structured data using modern data and AI tools.

## Architecture

### Data Layer (Snowflake)

- Normalized data model for movies, genres, credits, and keywords
- Vector embeddings stored directly in Snowflake using ARRAY type
- Custom similarity search functions using cosine similarity
- Efficient data retrieval using Snowflake's optimization features

### AI Layer (LangChain + OpenAI)

- Semantic search using OpenAI embeddings
- Conversational interface using ChatGPT
- Context-aware responses using movie metadata
- Intelligent movie recommendations based on natural language descriptions

### User Interface (Streamlit)

- Clean, modern web interface
- Real-time semantic search
- Interactive chat functionality
- Detailed movie information display

## Key Features

- Natural language movie search
- Semantic similarity-based recommendations
- Conversational movie exploration
- Rich movie metadata integration
- Vector similarity search in Snowflake

## Technical Stack

- **Database:** Snowflake
- **AI/ML:** LangChain, OpenAI
- **Frontend:** Streamlit
- **Language:** Python 3.8+
- **Key Libraries:**
  - `snowflake-connector-python`
  - `langchain`
  - `openai`
  - `streamlit`
  - `python-dotenv`

## Project Structure

```plaintext
imdb-agent/
├── agent/
│   ├── config/
│   │   └── snowflake_config.py
│   └── src/
│       ├── semantic_agent.py
│       └── snowflake_connector.py
├── snowflake/
│   ├── procedures/
│   │   └── generate_embeddings.sql
│   └── tables/
│       ├── create_tables.sql
│       └── load_data.sql
├── app.py
├── requirements.txt
└── .env.template
```

## Getting Started

1. Clone the repository
2. Copy `.env.template` to `.env` and fill in your credentials
3. Install dependencies: `pip install -r requirements.txt`
4. Run the Streamlit app: `streamlit run app.py`

## Current Status

- [x] Data model design and implementation
- [x] Snowflake integration and setup
- [x] Vector similarity search implementation
- [x] Basic agent functionality
- [x] OpenAI embeddings integration
- [x] Cosine similarity implementation
- [ ] Streamlit UI implementation
- [ ] Production deployment

### Recent Progress (May 5, 2025)

1. Successfully implemented embeddings generation using OpenAI's API
2. Created a robust data model in Snowflake with:
   - ARRAY type for storing embeddings
   - Efficient movie metadata storage
   - Unique constraints and primary keys
3. Developed Python pipeline for:
   - Generating embeddings from movie descriptions
   - Storing embeddings in Snowflake
   - Updating movies automatically
4. Implemented cosine similarity search with:
   - Custom SQL view for similarity calculations
   - Efficient vector operations using FLATTEN
   - Accurate semantic matching (0.82 similarity between Matrix and Inception)

## Next Steps

1. Add more test movies to validate similarity search
2. Implement the Streamlit UI for:
   - Movie search interface
   - Similarity results display
   - Movie details view
3. Add more movie metadata (genres, actors) to enhance recommendations
4. Enhance the conversational capabilities
5. Add user feedback and learning mechanisms

## Contributing

This is a proof of concept project. Feel free to fork and experiment with different approaches or improvements.

## License

MIT
