from flask import Flask, request, jsonify
from utils import get_embedding, insert_post_to_db, search_posts, close_db_connection

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search_post():
    """Search for posts by similarity to a given query."""
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    # Search for posts related to the query
    results = search_posts(query)

    # Format the response
    response = []
    for row in results:
        response.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "category": row[3],
            "similarity": row[5]
        })

    return jsonify({"results": response})

@app.route('/add_post', methods=['POST'])
def add_post():
    """Add a new post with its embedding to the database."""
    # Parse the request data
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    category = data.get("category")

    # Generate embedding for the new post
    combined_text = title + " " + description
    embedding = get_embedding(combined_text)

    # Insert the post into the database
    insert_post_to_db(title, description, category, embedding)

    return jsonify({"message": "Post added successfully!"})

@app.route('/close_db', methods=['POST'])
def close_connection():
    """Close the database connection."""
    close_db_connection()
    return jsonify({"message": "Database connection closed successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
