# Masterblog_API
## About

This is a little Python project to build an API with flask. It has a backend and frontend part. The frontend part will be interact with the flask API from the backend part. The backend part creating a blogging platform with options for get a list of all blog posts with a sorted option, add a new blog post, delete a post, update a post or search posts. Currently a post has three properties: id, title and content. There exists also an API documentation created with swagger_ui.

## Installation

To install this project, clone the repository and install dependencies in requirements.txt to using `pip install -r requirements.txt` for the installation.

## Usage

To use this project, run two files in separated terminals - `backend_app.py` and `frontend_app.py`. You can follow the given link in the terminal with the `frontend_app.py`. Currently you can put the URL of the backend on the blog posts website of the frontend and loads posts. Then you can see dummy posts which are saved in the variable `POSTS` in `backend_app.py`. You can use the buttons to add new posts or delete posts. For sorting, searching or updating posts you use the URL from the backend part or you use tools like postman.
Sorting example: `http://localhost:5002/api/posts?sort=title&direction=asc`
Search example: `http://localhost:5002/api/posts/search?title=first`
You can also use the API Documentation `HTTP://localhost:5002/api/docs`. (if `backand_app.py` is running)


## Contributing

If you'd like to contribute to this project, please follow these guidelines:
-   create a new branch to experiment with the code and possibly also open a new issue in case of additional content or wishes
-   if you find something interesting and want to share it, create a pull request
-   in case of bugs or problems, open a new issue and describe the bug/problem and mark it with labels