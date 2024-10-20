from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, SignupForm  # Import forms
from app.models import User
from pymongo import MongoClient

# Blueprint declaration
main = Blueprint("main", __name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.iris_database


# Home route
@main.route("/")
@login_required
def home():
    return render_template("index.html")


# Login route
@main.route("/login", methods=["GET", "POST"])
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
@main.route("/signup", methods=["GET", "POST"])
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
            return redirect(url_for("main.login"))
    return render_template("signup.html", form=form)


# Logout route
@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))
