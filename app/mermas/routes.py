from flask import render_template, flash, redirect, url_for, request
from app import db
from app.models import Merma, Repuesto # Importar modelos
from app.mermas import bp # Importar Blueprint
from app.mermas.forms import MermaForm # Importar formulario
from sqlalchemy.orm import joinedload

# --- Ruta para LISTAR todas las mermas ---
@bp.route('/')
@bp.route('/listar')
def listar_mermas():
    # Consultamos TODAS las mermas, ordenadas por fecha descendente
    # Cargamos eficientemente los datos del Repuesto relacionado
    mermas = Merma.query.options(
        joinedload(Merma.repuesto)
    ).order_by(Merma.fecha_merma.desc()).all()

    return render_template('mermas/listar_mermas.html', mermas=mermas, titulo='Historial de Mermas')

# --- Ruta para AÑADIR una nueva merma ---
@bp.route('/nueva', methods=['GET', 'POST'])
def nueva_merma():
    form = MermaForm()

    # --- Poblar SelectField de Repuestos ---
    # Mostramos solo repuestos CON STOCK > 0
    repuestos_con_stock = Repuesto.query.filter(Repuesto.stock_actual > 0).order_by(Repuesto.descripcion).all()
    form.repuesto_id.choices = [
        (r.id, f"{r.codigo_parte} - {r.descripcion} (Stock: {r.stock_actual})") for r in repuestos_con_stock
    ]
    # form.repuesto_id.choices.insert(0, (0, '-- Seleccione Repuesto --')) # Opcional

    if form.validate_on_submit():
        # Datos del formulario
        id_repuesto_sel = form.repuesto_id.data
        cantidad_perdida = form.cantidad.data
        motivo_opcional = form.motivo.data
        ot_opcional = form.orden_trabajo.data

        # Buscar el repuesto en la BD
        repuesto = Repuesto.query.get(id_repuesto_sel)

        if not repuesto:
             flash('Error: Repuesto no válido.', 'danger')
             return render_template('mermas/form_merma.html', form=form, titulo='Registrar Nueva Merma')

        # --- Validación de Stock ---
        if repuesto.stock_actual < cantidad_perdida:
            flash(f'Error: No se puede registrar merma de {cantidad_perdida}. Stock actual de "{repuesto.descripcion}" es {repuesto.stock_actual}', 'danger')
            return render_template('mermas/form_merma.html', form=form, titulo='Registrar Nueva Merma')
        else:
            # ¡Hay stock suficiente para registrar la merma!
            # 1. Crear la nueva Merma
            merma = Merma(
                repuesto_id=repuesto.id,
                cantidad=cantidad_perdida,
                motivo=motivo_opcional if motivo_opcional else None,
                orden_trabajo=ot_opcional if ot_opcional else None
                # Fecha se asigna por defecto
            )

            # 2. Disminuir el stock del Repuesto
            repuesto.stock_actual -= cantidad_perdida

            # 3. Guardar cambios en la BD
            db.session.add(merma)
            db.session.commit()

            flash(f'¡Merma de {cantidad_perdida} de "{repuesto.descripcion}" registrada!', 'success')
            return redirect(url_for('mermas.listar_mermas'))

    # Si es GET o el form no es válido (incluida la validación de stock)
    return render_template('mermas/form_merma.html', form=form, titulo='Registrar Nueva Merma')