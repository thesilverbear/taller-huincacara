# taller_ford_app/app/mermas/__init__.py
from flask import Blueprint

bp = Blueprint('mermas', __name__, template_folder='templates')

from app.mermas import routes