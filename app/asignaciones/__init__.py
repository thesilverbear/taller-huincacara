from flask import Blueprint

bp = Blueprint('asignaciones', __name__, template_folder='templates')

from app.asignaciones import routes