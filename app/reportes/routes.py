# taller_ford_app/app/reportes/routes.py
from flask import render_template, request # Importar request
from app import db
from app.models import Entrada, Asignacion, Merma, Repuesto, Trabajador # Importar todos los modelos necesarios
from app.reportes import bp
from app.reportes.forms import BusquedaForm
from sqlalchemy import or_, and_ # Para construir filtros complejos
from sqlalchemy.orm import joinedload

@bp.route('/buscar', methods=['GET']) # Usamos GET para búsquedas
def buscar():
    form = BusquedaForm(request.args) # Pasar request.args para repoblar el form

    # --- Poblar SelectFields del formulario ---
    # Trabajadores activos + opción "Todos"
    trabajadores_activos = Trabajador.query.filter_by(activo=True).order_by(Trabajador.nombre).all()
    form.trabajador_id.choices = [(0, '-- Todos --')] + [(t.id, t.nombre) for t in trabajadores_activos]
    # Todos los repuestos + opción "Todos"
    todos_repuestos = Repuesto.query.order_by(Repuesto.descripcion).all()
    form.repuesto_id.choices = [(0, '-- Todos --')] + [(r.id, f"{r.codigo_parte} - {r.descripcion}") for r in todos_repuestos]

    # --- Inicializar listas de resultados ---
    entradas_res = []
    asignaciones_res = []
    mermas_res = []

    # --- Construir filtros base (SI hay parámetros en la URL) ---
    # Verificamos si se envió el formulario comprobando si existe un parámetro (ej. 'submit') o cualquier otro campo del form
    if 'submit' in request.args or any(arg in request.args for arg in ['fecha_inicio', 'fecha_fin', 'trabajador_id', 'repuesto_id', 'orden_trabajo']):

        # Construir filtros base para cada modelo
        filtros_entrada = []
        filtros_asignacion = []
        filtros_merma = []

        # Filtro por Fecha Inicio
        if form.fecha_inicio.data:
            filtros_entrada.append(Entrada.fecha_entrada >= form.fecha_inicio.data)
            filtros_asignacion.append(Asignacion.fecha_asignacion >= form.fecha_inicio.data)
            filtros_merma.append(Merma.fecha_merma >= form.fecha_inicio.data)

        # Filtro por Fecha Fin (Ajuste: incluir todo el día)
        if form.fecha_fin.data:
             from datetime import datetime, time
             fecha_fin_ajustada = datetime.combine(form.fecha_fin.data, time(23, 59, 59))
             filtros_entrada.append(Entrada.fecha_entrada <= fecha_fin_ajustada)
             filtros_asignacion.append(Asignacion.fecha_asignacion <= fecha_fin_ajustada)
             filtros_merma.append(Merma.fecha_merma <= fecha_fin_ajustada)

        # Filtro por Repuesto (si se seleccionó uno específico)
        if form.repuesto_id.data and form.repuesto_id.data != 0:
            filtros_entrada.append(Entrada.repuesto_id == form.repuesto_id.data)
            filtros_asignacion.append(Asignacion.repuesto_id == form.repuesto_id.data)
            filtros_merma.append(Merma.repuesto_id == form.repuesto_id.data)

        # Filtro por Trabajador (solo aplica a Asignaciones)
        if form.trabajador_id.data and form.trabajador_id.data != 0:
            filtros_asignacion.append(Asignacion.trabajador_id == form.trabajador_id.data)

        # Filtro por Orden de Trabajo (aplica a Asignaciones y Mermas)
        # Usamos 'ilike' para búsqueda insensible a mayúsculas/minúsculas que contenga el texto
        if form.orden_trabajo.data:
             filtro_ot = f"%{form.orden_trabajo.data}%"
             filtros_asignacion.append(Asignacion.orden_trabajo.ilike(filtro_ot))
             filtros_merma.append(Merma.orden_trabajo.ilike(filtro_ot))


        # --- Ejecutar Consultas con los filtros ---
        # Usamos and_() para combinar todos los filtros de cada lista
        if filtros_entrada:
            entradas_res = Entrada.query.filter(and_(*filtros_entrada)).order_by(Entrada.fecha_entrada.desc()).all()
        # Si no hay filtros específicos para entradas pero sí otros filtros, podríamos querer mostrar todas las entradas dentro del rango de fechas/repuesto?
        # Por simplicidad, si no hay filtros específicos de entrada, no mostramos nada. Podemos ajustar esto.

        if filtros_asignacion:
            asignaciones_res = Asignacion.query.options(joinedload(Asignacion.repuesto), joinedload(Asignacion.trabajador)).filter(and_(*filtros_asignacion)).order_by(Asignacion.fecha_asignacion.desc()).all()

        if filtros_merma:
            mermas_res = Merma.query.options(joinedload(Merma.repuesto)).filter(and_(*filtros_merma)).order_by(Merma.fecha_merma.desc()).all()

    # Siempre renderizamos la plantilla, pasando el form y los resultados (que estarán vacíos si no se buscó)
    return render_template('reportes/buscar.html',
                           form=form,
                           entradas=entradas_res,
                           asignaciones=asignaciones_res,
                           mermas=mermas_res,
                           titulo='Buscar Registros / Reportes')