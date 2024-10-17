# Inicialización de la aplicación Flask
# Archivo principal para ejecutar la aplicación
# app.py
from flask import Flask, render_template, request
import joblib
import numpy as np
import database as dbase  # Importar la conexión de tu archivo database.py
from pymongo import MongoClient
import os

# Especificar la ruta correcta de la carpeta templates
app = Flask(
    __name__,
    template_folder=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "templates"
    ),
)


# Conectar a la base de datos local de MongoDB
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)

# Conectar a la base de datos
db = dbase.dbConnection()

# Cargar el modelo entrenado
model = joblib.load("iris_model.pkl")


# Ruta principal para mostrar el formulario
@app.route("/")
def home():
    return render_template("index.html")


# Ruta para manejar la predicción
@app.route("/predict", methods=["POST"])
def predict():
    sepal_length = float(request.form["sepal_length"])
    sepal_width = float(request.form["sepal_width"])
    petal_length = float(request.form["petal_length"])
    petal_width = float(request.form["petal_width"])

    # Crear el array de entrada para el modelo
    input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

    # Realizar la predicción
    prediction = model.predict(input_data)[0]

    # Guardar la consulta en la base de datos
    query = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width,
        "predicted_species": prediction,
    }
    db["iris_queries"].insert_one(query)

    # Renderizar la plantilla con el resultado de la predicción
    return render_template("index.html", prediction=prediction)


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True, port=4000)
