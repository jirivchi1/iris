# Rutas (endpoints) de la aplicación
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, SignupForm
from .models import User
from pymongo import MongoClient

# Conectar a la base de datos local de MongoDB
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client.iris_database

# Crear el blueprint principal
main = Blueprint("main", __name__)


@main.route("/")
@login_required
def home():
    return render_template("index.html")


@main.route("/predict", methods=["POST"])
@login_required
def predict():
    sepal_length = float(request.form["sepal_length"])
    sepal_width = float(request.form["sepal_width"])
    petal_length = float(request.form["petal_length"])
    petal_width = float(request.form["petal_width"])

    # Crear el array de entrada para el modelo
    input_data = [[sepal_length, sepal_width, petal_length, petal_width]]

    # Modelo de predicción
    model = joblib.load("iris_model.pkl")
    prediction = model.predict(input_data)[0]

    # Guardar la consulta en la base de datos
    query = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width,
        "predicted_species": prediction,
        "user_id": current_user.id,
    }
    db["iris_queries"].insert_one(query)

    return render_template("index.html", prediction=prediction)
