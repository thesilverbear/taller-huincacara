
from flask import render_template, flash, redirect, url_for, request
from app import db  # Importamos la instancia db desde app/__init__.py
from app.models import Trabajador # Importamos el modelo Trabajador
from app.core import bp # Importamos el Blueprint 'core'
from app.core.forms import TrabajadorForm # Importamos nuestro formulario
#importaciones para manejar repuestos:

from app.models import Repuesto # Asegúrate de que Repuesto esté importado
from app.core.forms import RepuestoForm # Importa el nuevo formulario

# --- Ruta para LISTAR todos los trabajadores ---
@bp.route('/trabajadores')
def listar_trabajadores():
    # Consultamos TODOS los trabajadores ordenados por nombre
    trabajadores = Trabajador.query.order_by(Trabajador.nombre).all()
    # Pasamos la lista de trabajadores a la plantilla
    return render_template('core/listar_trabajadores.html', trabajadores=trabajadores, titulo='Lista de Trabajadores')

# --- Ruta para AÑADIR un nuevo trabajador (muestra el form y procesa el envío) ---
@bp.route('/trabajadores/nuevo', methods=['GET', 'POST'])
def nuevo_trabajador():
    # Creamos una instancia de nuestro formulario
    form = TrabajadorForm()

    # Si el formulario se envió (POST) y es válido (pasó las validaciones)
    if form.validate_on_submit():
        # Creamos un nuevo objeto Trabajador con los datos del formulario
        trabajador = Trabajador(nombre=form.nombre.data, identificador=form.identificador.data)
        # Añadimos el nuevo trabajador a la sesión de la base de datos
        db.session.add(trabajador)
        # Guardamos los cambios en la base de datos
        db.session.commit()
        # Mostramos un mensaje de éxito al usuario (se mostrará en la siguiente página)
        flash(f'¡Trabajador "{trabajador.nombre}" añadido con éxito!', 'success')
        # Redirigimos al usuario a la lista de trabajadores
        return redirect(url_for('core.listar_trabajadores'))

    # Si es una solicitud GET (primera vez que se carga la página) o el form NO es válido,
    # mostramos la plantilla con el formulario.
    # WTForms se encargará de mostrar los errores de validación si los hubo.
    return render_template('core/form_trabajador.html', form=form, titulo='Añadir Trabajador')


# --- Ruta para CAMBIAR el estado activo/inactivo de un trabajador con un botón TOGGLE ---
@bp.route('/trabajadores/toggle_activo/<int:id>', methods=['POST']) # Usamos POST porque modifica datos
def toggle_activo_trabajador(id):
    # Buscamos al trabajador por su ID. Si no existe devuelve 404.
    trabajador = Trabajador.query.get_or_404(id)

    # Cambiamos el estado: si era True -> False, si era False -> True
    trabajador.activo = not trabajador.activo

    # Guardamos el cambio en la base de datos
    try:
        db.session.commit()
        # Preparamos mensaje de éxito según el nuevo estado
        estado = "activado" if trabajador.activo else "desactivado"
        flash(f'Trabajador "{trabajador.nombre}" ha sido {estado}.', 'success')
    except Exception as e:
        db.session.rollback() # Deshacer cambio si hay error al guardar
        flash(f'Error al cambiar el estado del trabajador: {str(e)}', 'danger')

    # Siempre redirigimos de vuelta a la lista de trabajadores
    return redirect(url_for('core.listar_trabajadores'))






##CODIGO PARA LAS FUNCIONALIDADES DE LOS RESPUESTOS: LISTAR, AÑADIR
# --- Ruta para LISTAR todos los repuestos ---
@bp.route('/repuestos')
def listar_repuestos():
    # Consultamos TODOS los repuestos ordenados por descripción
    repuestos = Repuesto.query.order_by(Repuesto.descripcion).all()
    # Pasamos la lista de repuestos a la plantilla
    return render_template('core/listar_repuestos.html', repuestos=repuestos, titulo='Lista de Repuestos')

# --- Ruta para AÑADIR un nuevo repuesto ---
@bp.route('/repuestos/nuevo', methods=['GET', 'POST'])
def nuevo_repuesto():
    form = RepuestoForm()
    if form.validate_on_submit():
        # Creamos el objeto Repuesto. El stock_actual será el stock_inicial ingresado.
        repuesto = Repuesto(codigo_parte=form.codigo_parte.data,
                            descripcion=form.descripcion.data,
                            stock_actual=form.stock_inicial.data) # Usamos stock_inicial del form
        db.session.add(repuesto)
        db.session.commit()
        flash(f'¡Repuesto "{repuesto.descripcion}" añadido con éxito!', 'success')
        return redirect(url_for('core.listar_repuestos')) # Redirige a la lista

    # Muestra el formulario (GET o si la validación falló)
    return render_template('core/form_repuesto.html', form=form, titulo='Añadir Repuesto')

