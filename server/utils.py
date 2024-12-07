import os
import numpy as np
import psycopg2
import google.generativeai as genai
from dotenv import load_dotenv
from urllib.parse import urlparse
from psycopg2.extras import Json

# Load environment variables
load_dotenv()

# Configure API key for Google Generative AI
genai.configure(api_key=os.getenv("API_KEY"))

# Retrieve the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Parse the DATABASE_URL to extract connection parameters
url = urlparse(DATABASE_URL)
db_name = url.path[1:]
db_user = url.username
db_password = url.password
db_host = url.hostname
db_port = url.port

# Connect to PostgreSQL (pgvector enabled)
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)
cursor = conn.cursor()

# Create the social schema and posts table if they don't exist
cursor.execute('''
CREATE SCHEMA IF NOT EXISTS social;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS social.posts (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    category TEXT,
    embedding VECTOR(384) -- Vector size based on the embedding model dimension
)
''')
conn.commit()

def get_embedding(text):
    """Generate embedding using Google Gemini."""
    result = genai.embed_content(
        model="models/text-embedding-004",  # Specify the embedding model
        content=text,
        output_dimensionality=384
    )
    return np.array(result["embedding"])

def insert_post_to_db(title, description, category, embedding):
    """Insert a post with its embedding into the database."""
    cursor.execute('''
    INSERT INTO social.posts (title, description, category, embedding)
    VALUES (%s, %s, %s, %s)
    ''', (title, description, category, embedding.tolist()))
    conn.commit()

def search_posts(query, top_n=5):
    """Search for posts by similarity to the query embedding."""
    query_embedding = get_embedding(query)

    # Perform the search using pgvector similarity( semantic Distance b/w query embedding and DB rows embedding)
    cursor.execute('''
    SELECT id, title, description, category, embedding,
           embedding <=> %s AS similarity
    FROM social.posts
    ORDER BY similarity
    LIMIT %s
    ''', (Json(query_embedding.tolist()), top_n))

    results = cursor.fetchall()
    return results

def close_db_connection():
    """Close the database connection."""
    cursor.close()
    conn.close()
