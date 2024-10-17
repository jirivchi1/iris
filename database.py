# Configuración y conexión a MongoDB
# database.py
from pymongo import MongoClient

# URI local para MongoDB
uri = "mongodb://localhost:27017/"  # URI local para la conexión a MongoDB


# Función para obtener la conexión a la base de datos
def dbConnection():
    try:
        client = MongoClient(uri)
        db = client["iris_database"]  # Conectar a la base de datos "iris_database"
        return db
    except Exception as e:
        print(f"Error de conexión con la base de datos: {e}")
        return None
