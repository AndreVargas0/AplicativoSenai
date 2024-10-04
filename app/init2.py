from flask import Flask,render_template,request,jsonify,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from aluno import Aluno
from datetime import datetime
from diariobordo import Diariobordo
import os

app = Flask(__name__)

import urllib.parse

from gtts import gTTS

import os

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
        return render_template('diariobordo.html', ra=ra, nome=nome,id=id)
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

@app.route('/diario', methods=["POST"])
def registar__diario():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'audio':
                audio_path = None
                texto = request.form['texto']
                idioma = 'pt'
                tts = gTTS(text=texto, lang=idioma)

                # Obtenha o diretório atual do aplicativo Flask
                base_dir = os.path.abspath(os.path.dirname(__file__))
                static_dir = os.path.join(base_dir, 'static')

                # Caminho completo do arquivo de áudio
                audio_filename = 'audio_exemplo.mp3'
                audio_full_path = os.path.join(static_dir, audio_filename)

                # Salve o áudio
                tts.save(audio_full_path)

                # Gere o URL do áudio
                audio_path = url_for('static', filename=audio_filename)
                return render_template('diariobordo3.html', audio_path=audio_path)
        
        elif action == 'diario_banco':
                pass

@app.route('/teste')
def teste():
    return render_template('diario.html')


@app.route('/teste3', methods=['POST'])
def teste3():
    texto = request.form.get('texto')
    idioma = 'pt'

    if not texto:
        return '', 400  # Retorna erro 400 se o texto não for fornecido
    
    try:
        tts = gTTS(text=texto, lang=idioma)

        # Define paths
        base_dir = os.path.abspath(os.path.dirname(__file__))
        static_dir = os.path.join(base_dir, 'static')
        audio_filename = 'audio_exemplo.mp3'
        audio_full_path = os.path.join(static_dir, audio_filename)

        # Salva o arquivo de áudio
        tts.save(audio_full_path)

        # Define o caminho do arquivo de áudio para o template
        audio_path = f'/static/{audio_filename}'

        return render_template('diario.html', audio_path=audio_path)

    except Exception as e:
        return str(e), 500  # Retorna erro 500 em caso de exceção

@app.route('/teste3', methods=['POST'])
def teste3():
    texto = request.form.get('texto')
    idioma = 'pt'

    if not texto:
        return '', 400  # Retorna erro 400 se o texto não for fornecido

    try:
        tts = gTTS(text=texto, lang=idioma)

        # Define paths
        base_dir = os.path.abspath(os.path.dirname(__file__))
        static_dir = os.path.join(base_dir, 'static')
        audio_filename = 'audio_exemplo.mp3'
        audio_full_path = os.path.join(static_dir, audio_filename)

        # Salva o arquivo de áudio
        tts.save(audio_full_path)

        # Verifica qual botão foi pressionado
        action = request.form.get('action')

        if action == 'gerar_audio_e_salvar':
            # Cria uma nova sessão
            session = Session()

            # Obtém data e hora atuais
            datahora_atual = datetime.now()

            # Cria uma nova instância de DiarioBordo
            novo_diario = DiarioBordo(texto=texto, data=data_atual, hora=hora_atual)

            # Aqui você deve adicionar o objeto `novo_diario` à sua lógica de inserção no banco
            # (considerando que você tenha uma tabela correspondente em seu banco de dados).
            try:
                # Adiciona o novo registro à tabela
                session.execute(
                    "INSERT INTO diariobordo (texto, data, hora) VALUES (:texto, :data, :hora)",
                    {'texto': novo_diario.texto, 'data': novo_diario.data, 'hora': novo_diario.hora}
                )
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Erro ao salvar no banco de dados: {e}")
                return str(e), 500
            finally:
                session.close()

        # Define o caminho do arquivo de áudio para o template
        audio_path = f'/static/{audio_filename}'

        return render_template('diario.html', audio_path=audio_path)

    except Exception as e:
        return str(e), 500  # Retorna erro 500 em caso de exceção


app.run(debug=True)
