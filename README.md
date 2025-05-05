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
- [ ] Complete embeddings generation
- [ ] Streamlit UI implementation
- [ ] Production deployment

## Next Steps

1. Complete the embeddings generation in Snowflake
2. Implement the Streamlit UI
3. Add more sophisticated recommendation algorithms
4. Enhance the conversational capabilities
5. Add user feedback and learning mechanisms

## Contributing

This is a proof of concept project. Feel free to fork and experiment with different approaches or improvements.

## License

MIT
