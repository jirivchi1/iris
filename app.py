from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from app.routes import main  # Import your routes blueprint
from app.models import User  # Import your user model

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Change this to something secure

# Set up MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.iris_database

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "main.login"  # Blueprint view for login


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user_data = db["users"].find_one({"_id": user_id})
    if user_data:
        return User(user_data["_id"], user_data["username"], user_data["password"])
    return None


# Register the blueprint
app.register_blueprint(main)

# Run the application
if __name__ == "__main__":
    app.run(debug=True, port=4000)
