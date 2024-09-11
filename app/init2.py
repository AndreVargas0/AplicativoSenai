from flask import Flask,render_template,request,jsonify,redirect,url_for

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, MetaData

from sqlalchemy.ext.automap import automap_base
from aluno import Aluno

app = Flask(__name__)

import urllib.parse

user = 'root'
password = urllib.parse.quote_plus('senai@123')

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

@app.route('/logar', methods=['POST'])
def logar():
    ra = request.form['ra']
    aluno = session.query(Aluno).filter_by(ra=ra).first()
    
    if aluno:
        nome = aluno.nome
        return render_template('diariobordo.html', ra=ra, nome=nome)
    else:
        mensagem = "RA INVALIDA"
        return render_template('index.html', mensagem=mensagem)
    

@app.route('/redirect_back')
def redirect_back():
    referrer = request.headers.get('Referer', url_for('home'))
    return redirect(referrer)

@app.route('/criaraluno', methods=['POST'])
def criar():
    
    ultimo_ra = session.query(Aluno.ra).order_by(Aluno.ra.desc()).first()  
    ra = str(int(ultimo_ra[0]) + 1).zfill(8)

    nome = request.form['nome']
    tempoestudo = int(request.form['tempoestudo'])
    rendafamiliar = float(request.form['rendafamiliar'])

    aluno_existente = session.query(Aluno).filter_by(nome=nome).first()
        
    if aluno_existente:
        mensagem_aluno = "Aluno já cadastrado no sistema."
        return render_template('novoaluno.html', mensagem_aluno=mensagem_aluno)
    
    aluno = Aluno(ra=ra, nome=nome, tempoestudo=tempoestudo, rendafamiliar=rendafamiliar)

    try:
      session.add(aluno) 
      session.commit()
    except:
      session.rollback()
      raise
    finally:
       session.close()

    mensagem2 = f"Cadastro efetuado com sucesso! O RA gerado para o aluno {nome} é {ra}."
    
    return render_template('novoaluno.html', mensagem2=mensagem2)


@app.route('/alunos', methods=['GET'])
def listar_alunos():
    try:
        nomes_alunos = [aluno.nome for aluno in session.query(Aluno.nome).all()]
    except Exception as e:
        session.rollback()
        mensagem = f"Erro ao tentar recuperar a lista de alunos: {str(e)}"
        return f"<p>{mensagem}</p>", 500
    
    finally:
        session.close()

    tabela_html = "<table border='1'><tr><th>Nome</th></tr>"
    
    for nome in nomes_alunos:
        tabela_html += f"<tr><td>{nome}</td></tr>"
    tabela_html += "</table>"


    return tabela_html, 200

@app.route('/consultar_ra', methods=['POST'])
def consultar_ra():
    nome = request.form['nome']
    
    aluno = session.query(Aluno).filter_by(nome=nome).first()
    
    if aluno:
        mensagem_recuperacao = f"O RA do aluno {aluno.nome} é {aluno.ra}."
    else:
        mensagem_recuperacao = "Aluno não encontrado. Verifique se o nome foi digitado corretamente."
    
    return render_template('index.html', mensagem_recuperacao=mensagem_recuperacao)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')


   
app.run(debug=True)
