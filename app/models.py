from datetime import datetime, timezone
from . import db # Importa el objeto db desde app/__init__.py

# cada Clase representa una tabla:

#Clase Trabajador y tabla trabajadores
class Trabajador(db.Model):
    __tablename__ = 'trabajadores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, index=True)
    identificador = db.Column(db.String(20), unique=True, nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    asignaciones = db.relationship('Asignacion', backref='trabajador', lazy='dynamic')

    def __repr__(self):
        return f'<Trabajador {self.nombre} ({self.identificador})>'

#Clase Repuesto y tabla repuestos
class Repuesto(db.Model):
    __tablename__ = 'repuestos'
    id = db.Column(db.Integer, primary_key=True)
    codigo_parte = db.Column(db.String(50), unique=True, nullable=False, index=True)
    descripcion = db.Column(db.String(255), nullable=False, index=True) # Incluye modelos compatibles
    stock_actual = db.Column(db.Integer, nullable=False, default=0)
    entradas = db.relationship('Entrada', backref='repuesto', lazy='dynamic')
    asignaciones = db.relationship('Asignacion', backref='repuesto', lazy='dynamic')
    mermas = db.relationship('Merma', backref='repuesto', lazy='dynamic')

    def __repr__(self):
        return f'<Repuesto {self.codigo_parte} - Stock: {self.stock_actual}>'

#Clase Entrada y tabla entradas
class Entrada(db.Model):
    __tablename__ = 'entradas'
    id = db.Column(db.Integer, primary_key=True)
    repuesto_id = db.Column(db.Integer, db.ForeignKey('repuestos.id'), nullable=False, index=True)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_entrada = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    def __repr__(self):
        return f'<Entrada ID: {self.id} - RepID: {self.repuesto_id} - Cant: {self.cantidad}>'

#Clase asignación y tabla asignaciones
class Asignacion(db.Model):
    __tablename__ = 'asignaciones'
    id = db.Column(db.Integer, primary_key=True)
    repuesto_id = db.Column(db.Integer, db.ForeignKey('repuestos.id'), nullable=False, index=True)
    trabajador_id = db.Column(db.Integer, db.ForeignKey('trabajadores.id'), nullable=False, index=True)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_asignacion = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)
    orden_trabajo = db.Column(db.String(50), nullable=True, index=True) # OT externa opcional

    def __repr__(self):
        return f'<Asignacion ID: {self.id} - RepID: {self.repuesto_id} - TrabID: {self.trabajador_id} - Cant: {self.cantidad} - OT: {self.orden_trabajo}>'

#Clase Merma y tabla mermas
class Merma(db.Model):
    __tablename__ = 'mermas'
    id = db.Column(db.Integer, primary_key=True)
    repuesto_id = db.Column(db.Integer, db.ForeignKey('repuestos.id'), nullable=False, index=True)
    cantidad = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(255), nullable=True)
    fecha_merma = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)
    orden_trabajo = db.Column(db.String(50), nullable=True, index=True) # OT externa opcional

    def __repr__(self):
        return f'<Merma ID: {self.id} - RepID: {self.repuesto_id} - Cant: {self.cantidad}>'
    