from flask import Flask,render_template,request

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, MetaData

from sqlalchemy.ext.automap import automap_base
from aluno import Aluno

app = Flask(__name__)

import urllib.parse

user = 'root'
password = urllib.parse.quote_plus('andre123')

host = 'localhost'
database = 'projetodiario1'
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'

engine = create_engine(connection_string)
metadata = MetaData()
metadata.reflect(engine)

Base = automap_base(metadata=metadata)
Base.prepare()

Aluno = Base.classes.aluno

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastrar_aluno():
    return render_template('novoaluno.html')

@app.route('/diario')
def abirdiario():
    return render_template('dirariobordo.html')

@app.route('/logar',methods=['POST'])
def logar():
    ra = request.form['ra']
    if ra == '12345619':
        return render_template('diariobordo.html',ra=ra)
    else:
        return f'O ra está errado'
    

@app.route('/criaraluno', methods=['POST'])
def criar():
    ra = request.form['ra']
    nome = request.form['nome']
    tempoestudo = int(request.form['tempoestudo'])
    rendafamiliar = float(request.form['rendafamiliar'])
    aluno = Aluno(ra=ra,nome=nome,tempoestudo=tempoestudo,rendafamiliar=rendafamiliar)
    session.add(aluno)
    session.commit()
    mensagem = "cadastro efetuado com sucesso"
    return render_template('index.html',msgbanco=mensagem)
   
app.run(debug=True)