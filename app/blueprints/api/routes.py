from flask import request
from . import api
from app import db
from app.models import Post, User
from .auth import basic_auth, token_auth



# Endpoint to get token - requires username/password
@api.route('/token')
@basic_auth.login_required
def get_token():
    auth_user = basic_auth.current_user()
    token = auth_user.get_token()
    return {'token': token}


# Endpoing to create a new User
@api.route('/users', methods=['POST'])
def create_user():
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    
    # Get the data from the request body
    data = request.json

    # Check to see if all of the required fiels are present
    required_fields = ['firstName', 'lastName', 'username', 'email', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    # Get the values from the data
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Check if there is already a user with username or email
    check_user = db.session.execute(db.select(User).where( (User.username==username) | (User.email==email) )).scalars().all()
    if check_user:
        return {'error': 'A user with that username and/or email already exists'}, 400
    
    # Create a new user
    new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
    # Add to the database
    db.session.add(new_user)
    db.session.commit()
    # return the dictionary/JSON version of the user
    return new_user.to_dict(), 201


# Endpoint to get user based on token
@api.route('/users/<int:id>', methods=["GET"])
@token_auth.login_required
def get_user(id):
    current_user = token_auth.current_user(id)
    return current_user.to_dict()

@api.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return [user.to_dict() for user in users]

# Endpoint to edit an exiting user
@api.route('/posts/<user_id>', methods=['PUT'])
@token_auth.login_required
def edit_user(user_id):
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    # Get the post from db
    user = db.session.get(User, user_id)
    if user is None:
        return {'error': f"User with an ID of {user_id} does not exist"}, 404
    data = request.json
    for field in data:
        if field in {'first_name', 'last_name', 'username', 'email'}:
            setattr(user, field, data[field])
    db.session.commit()
    return user.to_dict()

# Endpoint to delete an exiting user
@api.route('/users/<user_id>', methods=["DELETE"])
@token_auth.login_required
def delete_user(user_id):
    # Get the user from db
    user = db.session.get(User, user_id)
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    return {'success': f"{user.username} has been deleted"}


# Endpoint to get all posts
@api.route('/posts', methods=["GET"])
def get_posts():
    posts = db.session.execute(db.select(Post)).scalars().all()
    return [post.to_dict() for post in posts]

# Endpoint to get a post by ID
@api.route('/posts/<post_id>')
def get_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        return {'error': f'Post with an ID of {post_id} does not exist'}, 404
    return post.to_dict()

# Endpoint to create a new post
@api.route('/posts', methods=['POST'])
@token_auth.login_required
def create_post():
    # Check to see if that request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    # Get the data from the request body
    data =  request.json
    # Validate incoming data
    required_fields = ['title', 'body']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    # Get data from the body (we know the data is a dictionary)
    title = data.get('title')
    body = data.get('body')
    image_url = data.get('imageUrl')
    # Get the user
    current_user = token_auth.current_user()
    
    # Create a new Post to add to the database
    new_post = Post(title=title, body=body, image_url=image_url, user_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()
    return new_post.to_dict(), 201

# Endpoint to edit an exiting post
@api.route('/posts/<post_id>', methods=['PUT'])
@token_auth.login_required
def edit_post(post_id):
    # Check to see that the request body is JSON
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    # Get the post from db
    post = db.session.get(Post, post_id)
    if post is None:
        return {'error': f"Post with an ID of {post_id} does not exist"}, 404
    # Make sure authenticated user is the post author
    current_user = token_auth.current_user()
    if post.author != current_user:
        return {'error': 'You do not have permission to edit this post'}, 403
    data = request.json
    for field in data:
        if field in {'title', 'body', 'imageUrl'}:
            if field == 'imageUrl':
                setattr(post, 'image_url', data[field])
            else:
                setattr(post, field, data[field])
    db.session.commit()
    return post.to_dict()

# Endpoint to delete an exiting post
@api.route('/posts/<post_id>', methods=["DELETE"])
@token_auth.login_required
def delete_post(post_id):
    # Get the post from db
    post = db.session.get(Post, post_id)
    if post is None:
        return {'error': f'Post with an ID of {post_id} does not exist'}, 404
    # Make sure authenticated user is the post author
    current_user = token_auth.current_user()
    if post.author != current_user:
        return {'error': 'You do not have permission to delete this post'}, 403
    # Delete the post
    db.session.delete(post)
    db.session.commit()
    return {'success': f"{post.title} has been deleted"}