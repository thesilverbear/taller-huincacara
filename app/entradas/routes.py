from flask import render_template, flash, redirect, url_for, request
from app import db
from app.models import Entrada, Repuesto # Importamos ambos modelos
from app.entradas import bp # Importamos el Blueprint 'entradas'
from app.entradas.forms import EntradaForm # Importamos el formulario

# --- Ruta para LISTAR todas las entradas ---
@bp.route('/') 
@bp.route('/listar') # Podemos tener alias
def listar_entradas():
    # Consultamos TODAS las entradas, ordenadas por fecha descendente (más nuevas primero)
    # Usamos .options(joinedload(Entrada.repuesto)) para cargar eficientemente los datos del repuesto relacionado
    from sqlalchemy.orm import joinedload # Importar joinedload aquí
    entradas = Entrada.query.options(joinedload(Entrada.repuesto)).order_by(Entrada.fecha_entrada.desc()).all()
    # Pasamos la lista de entradas a la plantilla
    return render_template('entradas/listar_entradas.html', entradas=entradas, titulo='Historial de Entradas')

# --- Ruta para AÑADIR una nueva entrada ---
@bp.route('/nueva', methods=['GET', 'POST'])
def nueva_entrada():
    form = EntradaForm()

    # --- Poblar el SelectField de Repuestos ---
    # Necesitamos obtener todos los repuestos para llenar el desplegable.
    # Creamos una lista de tuplas: (id_repuesto, 'Codigo - Descripción')
    form.repuesto_id.choices = [
        (r.id, f"{r.codigo_parte} - {r.descripcion}") for r in Repuesto.query.order_by(Repuesto.descripcion).all()
    ]


    if form.validate_on_submit():
        # 1. Obtener el repuesto seleccionado de la BD
        repuesto_seleccionado = Repuesto.query.get(form.repuesto_id.data)

        if repuesto_seleccionado:
            # 2. Crear el nuevo registro de Entrada
            entrada = Entrada(repuesto_id=repuesto_seleccionado.id, # o form.repuesto_id.data
                              cantidad=form.cantidad.data)
                              # La fecha se asigna por defecto en el modelo

            # 3. Actualizar el stock del repuesto seleccionado
            repuesto_seleccionado.stock_actual += form.cantidad.data

            # 4. Añadir ambos cambios a la sesión y guardar
            db.session.add(entrada)
            db.session.commit()

            flash(f'¡Entrada de {form.cantidad.data} unidad(es) de "{repuesto_seleccionado.descripcion}" registrada!', 'success')
            return redirect(url_for('entradas.listar_entradas'))
        else:
            # Esto no debería pasar si el form se pobló correctamente, pero por si acaso
            flash('Error: Repuesto seleccionado no encontrado.', 'danger')

    # Si es GET o el form no es válido
    return render_template('entradas/form_entrada.html', form=form, titulo='Registrar Nueva Entrada')