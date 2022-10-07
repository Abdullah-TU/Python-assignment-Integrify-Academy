# Libraries
from webbrowser import get
from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash
from src.models.models import update_user_password_by_id,check_if_user_exist_in_database,create_new_user,get_user_by_email
from flask_jwt_extended import jwt_required, get_jwt_identity, create_refresh_token, create_access_token
from datetime import datetime
from src.constants.Constants import base_url
from src.DTO.ServerResponseDTO import get_server_response

# Auth controller blue print to be use in app.py in order to make connection.
authController = Blueprint("authController", __name__, url_prefix=base_url)


# Signup method in auth controller add new user in database.
@authController.post('/signup')
def Signup():
    # Get email or password from request body
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    # If email or password are empty then send bad request error
    if email == '' or password == '':
        return get_server_response(status=0, msg="email or password is required in order to register")

    # If user already present in data base then bad request error
    if check_if_user_exist_in_database(email=email):
        return get_server_response(status=0, msg="User Aleardy present with this email in database")

    # Create password hash
    hash = generate_password_hash(password)

    # Create a new user in database
    create_new_user(email, hash)

    # Send ok response to the user
    return get_server_response(status=1, msg="User register Successfully")


## sign in api for user
@authController.post('/signin')
def SignIn():
    # Get email or password from request body
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    # If email or password are empty then send bad request error
    if email == '' or password == '':
        return get_server_response(status=0, msg="email or password is required in order to login")

    user = get_user_by_email(email=email)

    # If user exists:
    if user:
        # Check if password is correct:
        CheckPassword = check_password_hash(user.Password, password)

        # If password hash match the stored data
        if CheckPassword:
            # Generate token
            access = create_access_token(identity=user.id)

            # Return access token
            return get_server_response(status=1, msg="User Logged in successfull", data=
            {
                'token': access,
                'email': user.Email,
                'id': user.id
            }
                                       )

    return get_server_response(status=0, msg="Email or password do not match")


@authController.put('/changePassword')
# Require access token from current loged in user
@jwt_required()
def ChangePassword():
    # Get the id of current user
    current_user = get_jwt_identity()

    # Receive new password in json format from the user
    password = request.json.get('password', '')

    # Check if no password is porvided
    if password == '':
        return get_server_response(status=0, msg="password cannot be empty")

    # Update the new password
    user = update_user_password_by_id(current_user, generate_password_hash(password))

    return get_server_response(status=1, msg="password changed successfully", data={'email': user.Email})
