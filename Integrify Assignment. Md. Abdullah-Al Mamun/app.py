# Libraries

from flask import Flask
import os
from flask_jwt_extended import JWTManager
from src.controllers.authController import authController
from src.controllers.todoController import todosController
from src.models.models import db ,connect_db
from dotenv import load_dotenv
load_dotenv()

# Declare flask app
app = Flask(__name__)

url = os.environ.get("DB_URL")
# Add flask app config from environment variables
app.config.update(
    SECRET_KEY=os.environ.get("FLASK_SECRET_KEY"),
    SQLALCHEMY_DATABASE_URI=os.environ.get("DB_URL"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')

        
)
  

connect_db(app)
# Create the tables in database if tables are not available as we are using
# Code first approach
with app.app_context():

    db.create_all()

# Initialize the jwt manager in app
JWTManager(app)

# Add controller of auth and todo in app
app.register_blueprint(authController)
app.register_blueprint(todosController)

if __name__ == "__main__":

    app.run(debug=True , port=8200)