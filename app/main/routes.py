from flask import render_template 
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    # Para renderizar index.html:
    return render_template('index.html', titulo="Inicio")