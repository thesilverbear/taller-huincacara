# taller_ford_app/run.py
from app import create_app # Importa la función factory desde app/__init__.py

# Crea la instancia de la aplicación llamando a la factory
app = create_app()

if __name__ == '__main__':
    # Ejecuta el servidor de desarrollo de Flask, puerto por defecto port 5000 se puede modificar

    app.run(host='0.0.0.0')
