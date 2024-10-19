from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import numpy as np
import database as dbase
from pymongo import MongoClient
from forms import LoginForm, SignupForm  # Import your forms
from routes import main  # Import your routes

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Change this to a secure secret key

# Set up MongoDB connection
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = dbase.dbConnection()

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Load the trained model
model = joblib.load("iris_model.pkl")


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user_data = db["users"].find_one({"_id": user_id})
    if user_data:
        return User(user_data["_id"], user_data["username"], user_data["password"])
    return None


# Register the routes blueprint
app.register_blueprint(main)


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db["users"].find_one({"username": form.username.data})
        if user and check_password_hash(user["password"], form.password.data):
            user_obj = User(user["_id"], user["username"], user["password"])
            login_user(user_obj)
            return redirect(url_for("main.home"))
        else:
            flash("Invalid username or password")
    return render_template("login.html", form=form)


# Signup route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = db["users"].find_one({"username": form.username.data})
        if existing_user:
            flash("Username already exists")
        else:
            hashed_password = generate_password_hash(
                form.password.data, method="sha256"
            )
            db["users"].insert_one(
                {"username": form.username.data, "password": hashed_password}
            )
            flash("Account created successfully. Please log in.")
            return redirect(url_for("login"))
    return render_template("signup.html", form=form)


# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=4000)
