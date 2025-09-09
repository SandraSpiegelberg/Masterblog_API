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
    sort = request.args.get('sort')
    direction = request.args.get('direction')

    accept_sort_para = {'title', 'content'}
    accept_direction_para = {'asc', 'desc'}

    if sort and direction:
        if sort in accept_sort_para and direction in accept_direction_para:
            reverse = True if direction == 'desc' else False
            sorted_posts = sorted(POSTS, key=lambda post: post[sort], reverse=reverse)
            return jsonify(sorted_posts)
        else:
            return jsonify({'error': 'Invalid sort or direction parameter'}), 400
    elif not sort and not direction:
        return jsonify(POSTS)
    else:
        return jsonify({'error': 'Boath sort and direction parameters are required.'}), 400


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


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Function to update a post by ID."""
    for post in POSTS:
        if post['id'] == post_id:
            post.update(request.get_json())
            return jsonify(post), 200
    return jsonify({'message': f'Post with id {post_id} was not found.'}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Function to search posts by title."""
    title = request.args.get('title', '').lower()
    content = request.args.get('content', '').lower()
    search_lst = []

    for post in POSTS:
        match_title =  title in post['title'].lower() if title else True
        match_content = content in post['content'].lower() if content else True

        if match_title and match_content:
            search_lst.append(post)

            
    return jsonify(search_lst), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
