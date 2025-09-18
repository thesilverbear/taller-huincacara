
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import Trabajador # Importamos el modelo para validaciones
#nuevas adiciones:
from wtforms import StringField, SubmitField, IntegerField # Asegúrate de añadir IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange # Añade NumberRange
from app.models import Repuesto # Importa el modelo Repuesto



class TrabajadorForm(FlaskForm):
    nombre = StringField('Nombre del Trabajador',
                       validators=[DataRequired(message="El nombre es obligatorio."), Length(min=3, max=100)])
    identificador = StringField('ID',
                       validators=[DataRequired(message="El legajo es obligatorio."), Length(min=1, max=20)])
    # Podríamos añadir 'activo' si quisiéramos editarlo, por ahora no en el 'crear'
    # activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar Trabajador')

    # --- Validación para evitar IDs duplicados ---
    def validate_identificador(self, identificador):
        # Comprueba si ya existe un trabajador con este ID en la DDBB
        # Necesitamos acceder al modelo Trabajador para esto
        trabajador = Trabajador.query.filter_by(identificador=identificador.data).first()
        if trabajador:
            raise ValidationError('Ya existe un trabajador con este legajo. Por favor, use uno diferente.')
        

# --- Formulario para Repuestos ---
class RepuestoForm(FlaskForm):
    codigo_parte = StringField('Código de Parte',
                             validators=[DataRequired(message="El código es obligatorio."), Length(min=1, max=50)])
    descripcion = StringField('Descripción (incluir modelos compatibles, ej: Pastillas Freno Ford Ranger 06-10)',
                            validators=[DataRequired(message="La descripción es obligatoria."), Length(min=5, max=255)])
    # Para el stock inicial, usaremos IntegerField
    stock_inicial = IntegerField('Stock Inicial', default=0,
                                 validators=[NumberRange(min=0, message="El stock no puede ser negativo.")])
    submit = SubmitField('Guardar Repuesto')

    # --- Validación para evitar códigos de parte duplicados ---
    def validate_codigo_parte(self, codigo_parte):
        # Verifica si ya existe un repuesto con este código
        repuesto = Repuesto.query.filter_by(codigo_parte=codigo_parte.data).first()
        if repuesto:
            raise ValidationError('Ya existe un repuesto con este Código de Parte. Por favor, use uno diferente.')