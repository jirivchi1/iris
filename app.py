from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
import joblib
import numpy as np
import database as dbase  # Importar la conexión de tu archivo database.py
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# Conectar a la base de datos local de MongoDB
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = dbase.dbConnection()

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Cambia esto por algo seguro

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirigir a login si no está autenticado

# Modelo de usuario
class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password_hash = password

# Cargar el modelo entrenado
model = joblib.load("iris_model.pkl")

# Ruta principal para mostrar el formulario
@app.route("/")
@login_required
def home():
    return render_template("index.html")

# Ruta para manejar la predicción
@app.route("/predict", methods=["POST"])
@login_required
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
        "user_id": current_user.id
    }
    db["iris_queries"].insert_one(query)

    # Renderizar la plantilla con el resultado de la predicción
    return render_template("index.html", prediction=prediction)

# Cargar el usuario desde la base de datos
@login_manager.user_loader
def load_user(user_id):
    user_data = db["users"].find_one({"_id": user_id})
    if user_data:
        return User(user_data["_id"], user_data["username"], user_data["password"])
    return None

# Ruta de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = db["users"].find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            user_obj = User(user["_id"], user["username"], user["password"])
            login_user(user_obj)
            return redirect(url_for("home"))
        else:
            flash("Usuario o contraseña incorrectos")

    return render_template("login.html")

# Ruta de logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Ruta de registro
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password, method='sha256')

        # Verificar si el usuario ya existe
        if db["users"].find_one({"username": username}):
            flash("El usuario ya existe")
        else:
            db["users"].insert_one({"username": username, "password": hashed_password})
            flash("Usuario registrado exitosamente. Inicia sesión.")
            return redirect(url_for("login"))

    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True, port=4000)
