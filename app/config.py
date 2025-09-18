import os
from dotenv import load_dotenv #Para cargar el archivo .env desde la raíz

# Encuentra la ruta absoluta al directorio raíz (root))
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# Carga el archivo .env desde root
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Clave secreta para proteger sesiones y otros datos
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'deberia-cambiar-esta-clave-por-defecto-en-produccion' #En este caso es "mequierotitular"

    # Configuración de la base de datos desde la variable de entorno 'mysql+mysqlconnector://root:pass@localhost/taller_ford_db'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # Desactiva esta característica de Flask-SQLAlchemy que no se usará y consume demasiados recursos:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    