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
database = 'projetoloja'
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'

engine = create_engine(connection_string)
metadata = MetaData()
metadata.reflect(engine)

Base = automap_base(metadata=metadata)
Base.prepare()

cliente = Base.classes.cliente

Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/novocliente')
def cadastrar_cliete():
    nome = request.form['nome']
    telefone = int(request.form['telefone'])
    email = request.form['email']
    senha = request.form['senha']
    
 
    cliente = cliente(nome=nome, telefone=telefone,email=email,senha=senha)
    try:
      session.add(cliente) 
      session.commit()
    except:
      session.rollback()
      raise
    finally:
       session.close()
    mensagem = f"Cadastro do cliente {nome} efetuado com sucesso!"   

@app.route('/novoservico')
def cadastrar_servico():
    servico = request.form['servico']
    valor = request.form['valor']
    novoservico = novoservico(servico=servico, valor=valor)
    try:
      session.add(novoservico) 
      session.commit()
    except:
      session.rollback()
      raise
    finally:
       session.close()
    mensagem2 = f"O {servico} foi cadastrado com sucesso no sistemas!"   
    return render_template('cadastro.html', mensagem2=mensagem2)


@app.route('/novoagendamento')
def novo_agendamento():
    data = request.form['data']
    hora = request.form['hora']
    cliente = request.form['cliente']
    servico = request.form['servico']
    funcionario = request.form['funcionario'] 
    novoagendamento = novoagendamento(data=data, hora=hora,cliente=cliente,servico=servico,funcionario=funcionario)
    try:
      session.add(agendamento) 
      session.commit()
    except:
      session.rollback()
      raise
    finally:
       session.close() 
    mensagem3 = f"O {servico} foi agendado para o dia {data}, horário {hora} com o(a) {funcionario}!"   
    return render_template('agendamento.html', mensagem3=mensagem3)



@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = usuario.query.filter_by(email=email).first()
        if usuario and usuario.senha == senha:
            login_usuario(usuario)
            mensagem4= 'Login feito com sucesso!'
            return render_template('home.html', mensagem4=mensagem4)
        else:
            mensagem5='Email ou senha errado'
            return render_template('login.html', mensagem5=mensagem5)


@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

app.run(debug=True)