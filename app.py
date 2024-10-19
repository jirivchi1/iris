from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from routes import main
from models import User
from forms import LoginForm, SignupForm

# Inicializar la aplicación Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Cambia esto por una clave segura

# Conectar a la base de datos local de MongoDB
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client.iris_database

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Registrar el blueprint
app.register_blueprint(main)


# Cargar el usuario desde la base de datos
@login_manager.user_loader
def load_user(user_id):
    user_data = db["users"].find_one({"_id": user_id})
    if user_data:
        return User(user_data["_id"], user_data["username"], user_data["password"])
    return None


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True, port=4000)
