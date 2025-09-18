from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, SubmitField, TextAreaField # Añadir TextAreaField
from wtforms.validators import DataRequired, NumberRange, Length, Optional
from app.models import Repuesto # Necesitamos Repuesto de app.models para validar stock

class MermaForm(FlaskForm):
    # SelectField para seleccionar el repuesto
    repuesto_id = SelectField('Repuesto', coerce=int, validators=[DataRequired(message="Debe seleccionar un repuesto.")])
    # Cantidad perdida
    cantidad = IntegerField('Cantidad Perdida/Dañada', validators=[DataRequired(message="La cantidad es obligatoria."), NumberRange(min=1, message="La cantidad debe ser al menos 1.")])
    # Motivo (opcional, usamos TextAreaField para más espacio)
    motivo = TextAreaField('Motivo de la Merma (Opcional)', validators=[Optional(), Length(max=255)])
    # Orden de Trabajo (opcional, si aplica)
    orden_trabajo = StringField('Orden de Trabajo (si aplica, Opcional)', validators=[Optional(), Length(max=50)])
    submit = SubmitField('Registrar Merma')

    # La validación de stock, al igual que en asignaciones, la haremos en la RUTA
    # para verificar el stock disponible justo antes de guardar.