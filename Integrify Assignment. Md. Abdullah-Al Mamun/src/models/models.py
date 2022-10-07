# Libraries
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.Enums.enums import status

# Make an sql alchemy object.
db = SQLAlchemy()


# Model for the user.
class Users(db.Model):
    # Table name as users
    __tablename__ = 'Users'
    # id column it must be the primary key.
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Email column must be unique so that only one user against an email.
    Email = db.Column(db.String(60), unique=True)
    # Password column in order to store password of the user
    Password = db.Column(db.String(200))
    # Created at column by default it will take current date and time
    CreatedAt = db.Column(db.DateTime, default=datetime.now())
    # Updated at column by default it will take current date and time
    UpdatedAt = db.Column(db.DateTime, default=datetime.now())
    # todos object in order to make one to many relation ship
    Todos = db.relationship('Todos')





# Model for the todos
class Todos(db.Model):
    # Set the table name as todos
    __tablename__ = 'Todos'
    # Id column must be unique and it is also a primary key
    Id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    # Name column having a string data type
    Name = db.Column(db.String())
    # Description column have a string data type
    Description = db.Column(db.String())
    # Foriegn key user id
    UserId = db.Column(db.Integer, db.ForeignKey('Users.id'))
    # Create at column by default it will take current date and time
    CreatedAt = db.Column(db.DateTime, default=datetime.now())
    # Updated at column by default it will take current date and time
    UpdatedAt = db.Column(db.DateTime, default=datetime.now())
    # Add column based upon the enum value by default value of todo will be not started
    status = db.Column(db.Enum(status), default=status.NotStarted)


# Method to check if existing user present in db
def check_if_user_exist_in_database(email):
    return Users.query.filter_by(Email=email).first() is not None


# Method to create new user
def create_new_user(email, password):
    user = Users(Email=email, Password=password)
    db.session.add(user)
    db.session.commit()

# Method to get user by email
def get_user_by_email(email):
    # query user from the database
    user = Users.query.filter_by(Email=email).first()
    return user

# Method to get user by id
def get_user_by_id(id):
    user = Users.query.filter_by(id=id).first()
    return user

# Method to update user by id
def update_user_password_by_id(id, newPassword):
    user = Users.query.filter_by(id=id).first()
    user.password = newPassword
    user.UpdatedAt = datetime.now()
    db.session.commit()
    return user

# Method to add new todo list items
def add_new_todo_item(name, description, userid, status):
    # create a todo item comprising given data
    todo_item = Todos(UserId=userid, Name=name,
                      Description=description, status=status)

    # Add todo item in the database
    db.session.add(todo_item)
    db.session.commit()
    return todo_item

# Method to get filter items
def get_todo_item_using_filter(userid, filter):
    # query database based on current user id AND the status
    todo_items = Todos.query.filter_by(
        UserId=userid, status=filter)

    return todo_items

# Method to get all todo items agains user id
def get_all_todo_items_against_userId(userid):
    return Todos.query.filter_by(UserId=userid)

# Method to get todo item by id
def get_todo_item_by_id(userid, id):
    return Todos.query.filter_by(UserId=userid, Id=id).first()

# Method to update the to do list items
def update_todo_item(todo_item, name, description, status_value):
    # if no name is provided keep original, if provided then update
    if name != '':
        todo_item.Name = name

    # If no description is provided keep original, if provided then update
    if description != '':
        todo_item.Description = description

    # If no status is provided keep original, if provided then update
    if status_value != '' and status_value in ['OnGoing', 'NotStarted', 'Completed']:
        todo_item.status = status_value

    # Update the update_at timestamp
    todo_item.UpdatedAt = datetime.now()

    # Commit changes to the database
    db.session.commit()

# Method to delete item from db
def delete_todo_item_from_db(todo_item):
    # Delete item
    db.session.delete(todo_item)

    # Commit changes to datanase
    db.session.commit()


# Method to connect with data base
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)