"""A simple Flask backend application for a blogging platform."""
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Function to get the posts."""
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Function to add a new post."""
    if request.method == 'POST':
        if not request.is_json or 'title' not in request.json or 'content' not in request.json:
            return jsonify({'error': 'Invalid input'}), 400

        new_post = request.get_json()
        new_post['id'] = max(post['id'] for post in POSTS) + 1 if POSTS else 1
        POSTS.append(new_post)
        return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Function to delete a post by ID."""
    for post in POSTS[:]:
        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'}), 200
    return jsonify({'message': f'Post with id {post_id} was not found.'}), 404



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
