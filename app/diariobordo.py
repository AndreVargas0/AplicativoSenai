from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DiarioBordo(db.Model):
    __tablename__ = 'diariobordo'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=True)
    datahora = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=True)
    fk_aluno_ra = db.Column(db.String(8), nullable=False)
    polaridade = db.Column(db.Text, nullable=True)

    def __init__(self, texto, fk_aluno_ra, polaridade=None):
        self.texto = texto
        self.fk_aluno_ra = fk_aluno_ra
        self.polaridade = polaridade