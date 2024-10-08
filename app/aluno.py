from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Aluno(db.Model):
    __tablename__ = 'aluno'  

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    ra = db.Column(db.String(8), unique=True, nullable=False)  # RA como CHAR(8)
    nome = db.Column(db.String(80))  # Nome
    tempoestudo = db.Column(db.Integer, nullable=False)  # Tempo de estudo
    rendafamiliar = db.Column(db.DECIMAL(10, 2))  # Renda familiar