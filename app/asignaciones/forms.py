
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Optional # Importar Optional
from app.models import Repuesto # Necesitamos Repuesto para validar stock

class AsignacionForm(FlaskForm):
    # SelectField para seleccionar el repuesto
    repuesto_id = SelectField('Repuesto', coerce=int, validators=[DataRequired(message="Debe seleccionar un repuesto.")])
    # SelectField para seleccionar el trabajador
    trabajador_id = SelectField('Trabajador', coerce=int, validators=[DataRequired(message="Debe seleccionar un trabajador.")])
    # Cantidad a asignar
    cantidad = IntegerField('Cantidad a Asignar', validators=[DataRequired(message="La cantidad es obligatoria."), NumberRange(min=1, message="La cantidad debe ser al menos 1.")])
    # Orden de Trabajo (opcional)
    orden_trabajo = StringField('Orden de Trabajo (Opcional)', validators=[Optional(), Length(max=50)]) # Optional() permite que esté vacío
    submit = SubmitField('Registrar Asignación')

  