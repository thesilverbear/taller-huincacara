from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class EntradaForm(FlaskForm):
    # Usamos SelectField para mostrar una lista desplegable de repuestos.
    # 'coerce=int' asegura que el valor seleccionado se trate como un número entero (el ID del repuesto).
    repuesto_id = SelectField('Repuesto', coerce=int, validators=[DataRequired(message="Debe seleccionar un repuesto.")])
    cantidad = IntegerField('Cantidad Recibida', validators=[DataRequired(message="La cantidad es obligatoria."), NumberRange(min=1, message="La cantidad debe ser al menos 1.")])
    submit = SubmitField('Registrar Entrada')
