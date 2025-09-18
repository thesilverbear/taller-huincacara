#Definiremos la lógica para listar asignaciones
# y manejar el formulario de nueva asignación, incluyendo la validación de stock y la actualización (resta) del mismo.

from flask import render_template, flash, redirect, url_for, request
from app import db
from app.models import Asignacion, Repuesto, Trabajador # Importar los 3 modelos
from app.asignaciones import bp # Importar el Blueprint
from app.asignaciones.forms import AsignacionForm # Importar el formulario
from sqlalchemy.orm import joinedload # Para carga eficiente

# --- Ruta para LISTAR todas las asignaciones ---
@bp.route('/')
@bp.route('/listar')
def listar_asignaciones():
    # Consultamos TODAS las asignaciones, ordenadas por fecha descendente
    # Cargamos eficientemente los datos relacionados de Repuesto y Trabajador
    asignaciones = Asignacion.query.options(
        joinedload(Asignacion.repuesto),
        joinedload(Asignacion.trabajador)
    ).order_by(Asignacion.fecha_asignacion.desc()).all()

    return render_template('asignaciones/listar_asignaciones.html', asignaciones=asignaciones, titulo='Historial de Asignaciones')

# --- Ruta para AÑADIR una nueva asignación ---
@bp.route('/nueva', methods=['GET', 'POST'])
def nueva_asignacion():
    form = AsignacionForm()

    # --- Poblar SelectFields ---
    # Repuestos: Solo mostrar repuestos CON STOCK > 0
    repuestos_con_stock = Repuesto.query.filter(Repuesto.stock_actual > 0).order_by(Repuesto.descripcion).all()
    form.repuesto_id.choices = [
        (r.id, f"{r.codigo_parte} - {r.descripcion} (Stock: {r.stock_actual})") for r in repuestos_con_stock
    ]
    # Trabajadores: Solo mostrar trabajadores ACTIVOS
    trabajadores_activos = Trabajador.query.filter_by(activo=True).order_by(Trabajador.nombre).all()
    form.trabajador_id.choices = [(t.id, t.nombre) for t in trabajadores_activos]



    if form.validate_on_submit():
        # Datos del formulario
        id_repuesto_sel = form.repuesto_id.data
        id_trabajador_sel = form.trabajador_id.data
        cantidad_a_asignar = form.cantidad.data
        ot_opcional = form.orden_trabajo.data

        # Buscar los objetos en la BD
        repuesto = Repuesto.query.get(id_repuesto_sel)
        trabajador = Trabajador.query.get(id_trabajador_sel) 

        if not repuesto or not trabajador:
             flash('Error: Repuesto o Trabajador no válido.', 'danger')
             # Volver a renderizar el form CON los datos que el usuario puso
             return render_template('asignaciones/form_asignacion.html', form=form, titulo='Registrar Nueva Asignación')

        # --- Validación de Stock ---
        if repuesto.stock_actual < cantidad_a_asignar:
            flash(f'Error: No hay suficiente stock de "{repuesto.descripcion}". Disponible: {repuesto.stock_actual}', 'danger')
            # Volver a renderizar el form CON los datos que el usuario puso
            return render_template('asignaciones/form_asignacion.html', form=form, titulo='Registrar Nueva Asignación')
        else:
            # ¡Hay stock! Proceder a registrar y actualizar
            # 1. Crear la nueva Asignación
            asignacion = Asignacion(
                repuesto_id=repuesto.id,
                trabajador_id=trabajador.id,
                cantidad=cantidad_a_asignar,
                orden_trabajo=ot_opcional if ot_opcional else None # Guardar None si está vacío
            )

            # 2. Disminuir el stock del Repuesto
            repuesto.stock_actual -= cantidad_a_asignar

            # 3. Guardar cambios en la BD
            db.session.add(asignacion)
            # db.session.add(repuesto) # No es necesario, SQLAlchemy rastrea el cambio
            db.session.commit()

            flash(f'¡Asignación de {cantidad_a_asignar} de "{repuesto.descripcion}" a "{trabajador.nombre}" registrada!', 'success')
            return redirect(url_for('asignaciones.listar_asignaciones'))

    # Si es GET o el form no es válido (incluida la validación de stock que hicimos arriba)
    return render_template('asignaciones/form_asignacion.html', form=form, titulo='Registrar Nueva Asignación')