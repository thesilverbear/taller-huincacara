from flask import Blueprint

bp = Blueprint('entradas', __name__, template_folder='templates')

from app.entradas import routes