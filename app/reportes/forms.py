# taller_ford_app/app/reportes/forms.py
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, DateField
from wtforms.validators import Optional, Length

class BusquedaForm(FlaskForm):
    # Campos de fecha opcionales
    fecha_inicio = DateField('Fecha Desde (Opcional)', format='%Y-%m-%d', validators=[Optional()])
    fecha_fin = DateField('Fecha Hasta (Opcional)', format='%Y-%m-%d', validators=[Optional()])

    # Desplegables opcionales (se poblarán en la ruta)
    # Usamos 0 como valor "Todos" o "Ninguno seleccionado"
    trabajador_id = SelectField('Trabajador (Opcional)', coerce=int, default=0, validators=[Optional()])
    repuesto_id = SelectField('Repuesto (Opcional)', coerce=int, default=0, validators=[Optional()])

    # Orden de trabajo opcional
    orden_trabajo = StringField('Orden de Trabajo (Opcional)', validators=[Optional(), Length(max=50)])

    # Botón de búsqueda
    submit = SubmitField('Buscar / Filtrar')

    # Nota sobre DateField: Requiere que el navegador soporte input type="date"
    # o que instales una dependencia adicional si quieres un widget de calendario.
    # Para simplicidad, confiaremos en el navegador. El formato %Y-%m-%d es clave.
    # Asegúrate de tener wtforms >= 3.0 o ajusta la importación si usas una versión anterior.