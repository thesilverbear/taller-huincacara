#imports:
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
import datetime 
import pytz 

db = SQLAlchemy()
#función para que tome la fecha UTC y la convierta a la hora en Chile:
def format_datetime_local(dt_utc, tz_name='America/Santiago', fmt='%Y-%m-%d %H:%M'):
    """Filtro Jinja para convertir UTC a zona horaria local y formatear."""
    if dt_utc is None:
        return 'N/A'
    try:
        local_tz = pytz.timezone(tz_name)
        if dt_utc.tzinfo is None:
             dt_utc = pytz.utc.localize(dt_utc)
        # Convertir a la zona horaria local con localize
        dt_local = dt_utc.astimezone(local_tz)
        return dt_local.strftime(fmt)
    except Exception:
         # En caso de error devolver la fecha original formateada (o un mensaje)
         try:
             return dt_utc.strftime(fmt)
         except:
             return str(dt_utc) # Fallback básico


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    app.jinja_env.filters['local_time'] = format_datetime_local

    # Registrar los blueprints después de inicializar db:
    from app.main import bp as main_bp
    app.register_blueprint(main_bp) # Sin prefijo'/' al ser ruta main

    from app.core import bp as core_bp
    app.register_blueprint(core_bp, url_prefix='/core') # Rutas url que comienzan con /core/

    from app.entradas import bp as entradas_bp
    app.register_blueprint(entradas_bp, url_prefix='/entradas') # Rutas url que comienzan con /entradas/

    from app.asignaciones import bp as asignaciones_bp
    app.register_blueprint(asignaciones_bp, url_prefix='/asignaciones') # Rutas url que comienzan con /asignaciones/

    from app.mermas import bp as mermas_bp
    app.register_blueprint(mermas_bp, url_prefix='/mermas') # Rutas url que comienzan con /mermas/

    from app.reportes import bp as reportes_bp
    app.register_blueprint(reportes_bp, url_prefix='/reportes') # Rutas url que comienzan con /reportes/

    
    from . import models # Importando modelos ANTES del create_all por si acaso

    with app.app_context():
        print("Creando tablas de base de datos si no existen...")
        db.create_all() # Esto crea las tablas definidas en models.py
        print("Tablas verificadas/creadas.")

    return app