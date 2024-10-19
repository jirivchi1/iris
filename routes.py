from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
import numpy as np
from app import model, db  # Import the model and db from app.py

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

    input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    prediction = model.predict(input_data)[0]

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
