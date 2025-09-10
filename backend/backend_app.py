"""A simple Flask backend application for a blogging platform."""
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Function to get the posts. The posts can be sorted by 
    title or content in ascending or descending order.
    :return: List of posts, possibly sorted"""
    sort = request.args.get('sort')
    direction = request.args.get('direction')

    accept_sort_para = {'title', 'content'}
    accept_direction_para = {'asc', 'desc'}

    if sort and direction:
        if sort in accept_sort_para and direction in accept_direction_para:
            reverse = True if direction == 'desc' else False
            sorted_posts = sorted(POSTS, key=lambda post: post[sort], reverse=reverse)
            return jsonify(sorted_posts)
        return jsonify({'error': 'Invalid sort or direction parameter'}), 400
    if not sort and not direction:
        return jsonify(POSTS)
    return jsonify({'error': 'Boath sort and direction parameters are required.'}), 400


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Function to add a new post.
    :return: The newly created post with its ID"""
    if not request.is_json or 'title' not in request.json or 'content' not in request.json:
        return jsonify({'error': 'Invalid input'}), 400

    new_post = request.get_json()
    new_post['id'] = max(post['id'] for post in POSTS) + 1 if POSTS else 1
    POSTS.append(new_post)
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Function to delete a post by ID.
    :param post_id: ID of the post to delete
    :return: Success message or error message if post not found"""
    for post in POSTS[:]:
        if post['id'] == post_id:
            POSTS.remove(post)
            return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'}), 200
    return jsonify({'message': f'Post with id {post_id} was not found.'}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Function to update a post by ID.
    :param post_id: ID of the post to update
    :return: Updated post or error message if post not found"""
    for post in POSTS:
        if post['id'] == post_id:
            post.update(request.get_json())
            return jsonify(post), 200
    return jsonify({'message': f'Post with id {post_id} was not found.'}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Function to search posts by title.
    :return: List of posts that match the search criteria"""
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
