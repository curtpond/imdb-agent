import os
from openai import OpenAI

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get API key from environment
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize the client
client = OpenAI(api_key=api_key)

# Test the API
try:
    response = client.embeddings.create(
        input="Hello, world!",
        model="text-embedding-ada-002"
    )
    print("Success! Embedding size:", len(response.data[0].embedding))
except Exception as e:
    print("Error:", str(e))
