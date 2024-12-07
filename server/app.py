from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
import os

app = Flask(__name__)

# Define the path for the locally saved model
local_model_path = "./models/all-MiniLM-L6-v2"

# Try to load the model from the local path, or fallback to downloading it
try:
    print(f"Trying to load the model from {local_model_path}...")
    if not os.path.exists(local_model_path):
        raise FileNotFoundError("Model folder not found.")
    
    # Load the local model
    model = SentenceTransformer(local_model_path)
    print("Successfully loaded the model from local storage.")

except (FileNotFoundError, Exception) as e:
    print(f"Error loading model locally: {e}")
    print("Falling back to downloading the model from Hugging Face...")
    
    # Fallback: Load the model from Hugging Face
    model_name = 'all-MiniLM-L6-v2'
    model = SentenceTransformer(model_name)
    print(f"Model {model_name} downloaded from Hugging Face.")

# Sample posts (these can be loaded from a database in production)
posts = [
    {"id": 1, "content": "Learn Next.js for modern web development."},
    {"id": 2, "content": "Introduction to semantic search and its applications."},
    {"id": 3, "content": "Building responsive UIs with Tailwind CSS."},
    {"id": 4, "content": "Using Flask for building microservices."},
    {"id": 5, "content": "Understanding Docker for containerized applications."}
]

# Pre-compute embeddings for all posts
post_embeddings = model.encode([post["content"] for post in posts], convert_to_tensor=True)

@app.route('/search', methods=['POST'])
def search():
    # Parse the query from the request
    data = request.get_json()
    query = data.get("query", "")

    # Encode the query
    query_embedding = model.encode(query, convert_to_tensor=True)

    # Compute cosine similarity
    similarities = util.cos_sim(query_embedding, post_embeddings)[0]

    # Get the top results
    top_results = sorted(
        [{"id": posts[i]["id"], "content": posts[i]["content"], "score": float(sim)} 
         for i, sim in enumerate(similarities)],
        key=lambda x: x["score"],
        reverse=True
    )[:5]

    # Return the results as JSON
    return jsonify(top_results)

if __name__ == '__main__':
    app.run(debug=True)