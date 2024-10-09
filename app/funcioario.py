from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    rg = db.Column(db.String(8), unique=True, nullable=False)  # RG como CHAR(8)
    nome = db.Column(db.String(100), nullable=False)  # Nome do funcionário
    setor = db.Column(db.String(50))  # Setor do funcionário
