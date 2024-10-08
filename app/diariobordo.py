from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DiarioBordo(db.Model):
    __tablename__ = 'diariobordo'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=True)
    datahora = db.Column(db.DateTime, nullable=True)  # Data e hora automáticas
    fk_aluno_ra = db.Column(db.String(10), db.ForeignKey('aluno.ra'), nullable=False)
    polaridade = db.Column(db.Text, nullable=True)

    def __init__(self, texto, fk_aluno_ra):
        self.texto = texto
        self.fk_aluno_ra = fk_aluno_ra
