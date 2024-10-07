from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from aluno import Aluno
from datetime import datetime
from gtts import gTTS
import os
import urllib.parse

app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = 'session_flask'
# Defina a chave secreta para a sessão do Flask
app.secret_key = 'andre123'

# Configuração do banco de dados MySQL
user = 'root'
password = urllib.parse.quote_plus('andre123')
host = 'localhost'
database = 'projetodiario1'
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'

engine = create_engine(connection_string)
metadata = MetaData()
metadata.reflect(engine)

# Automap Base
Base = automap_base(metadata=metadata)
Base.prepare()

# Mapeando as tabelas
Aluno = Base.classes.aluno
DiarioBordo = Base.classes.diariobordo

# Configurando o sessionmaker do SQLAlchemy
Session = sessionmaker(bind=engine)
db_session = Session()


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
    db_session = Session()
    ra = request.form['ra']
    aluno = db_session.query(Aluno).filter_by(ra=ra).first()
    
    if aluno:
        session['ra'] = aluno.ra
        session['nome'] = aluno.nome
        
        return redirect(url_for('diariobordo'))
    else:
        mensagem = "RA INVÁLIDA"
        return render_template('index.html', mensagem=mensagem)
    
# Rota da página do diário de bordo
@app.route('/Menu')
def diariobordo():
    if 'ra' in session and 'nome' in session:
        ra = session['ra']
        nome = session['nome']
        return render_template('menu.html', ra=ra, nome=nome)
    else:
        flash('Por favor, faça login primeiro.')
        return redirect(url_for('index'))
    
@app.route('/criaraluno', methods=['POST'])
def criar():
    
    ultimo_ra = db_session.query(Aluno.ra).order_by(Aluno.ra.desc()).first()  
    ra = str(int(ultimo_ra[0]) + 1).zfill(8)

    nome = request.form['nome']
    tempoestudo = int(request.form['tempoestudo'])
    rendafamiliar = float(request.form['rendafamiliar'])

    aluno_existente = db_session.query(Aluno).filter_by(nome=nome).first()
        
    if aluno_existente:
        mensagem_aluno = "Aluno já cadastrado no sistema."
        return render_template('novoaluno.html', mensagem_aluno=mensagem_aluno)
    
    aluno = Aluno(ra=ra, nome=nome, tempoestudo=tempoestudo, rendafamiliar=rendafamiliar)

    try:
        db_session.add(aluno) 
        db_session.commit()  # Use db_session aqui
    except Exception as e:
        db_session.rollback()
        # É uma boa prática logar o erro
        print(f"Erro ao cadastrar aluno: {e}")
        mensagem2 = "Erro ao cadastrar aluno. Tente novamente mais tarde."
        return render_template('novoaluno.html', mensagem2=mensagem2)

    mensagem2 = f"Cadastro efetuado com sucesso! O RA gerado para o aluno {nome} é {ra}."
    
    return render_template('novoaluno.html', mensagem2=mensagem2)


@app.route('/alunos', methods=['GET'])
def listar_alunos():
    try:
        nomes_alunos = [aluno.nome for aluno in db_session.query(Aluno.nome).all()]
    except Exception as e:
        db_session.rollback()
        mensagem = f"Erro ao tentar recuperar a lista de alunos: {str(e)}"
        return f"<p>{mensagem}</p>", 500
    
    finally:
        db_session.close()

    tabela_html = "<table border='1'><tr><th>Nome</th></tr>"
    
    for nome in nomes_alunos:
        tabela_html += f"<tr><td>{nome}</td></tr>"
    tabela_html += "</table>"


    return tabela_html, 200

@app.route('/consultar_ra', methods=['POST'])
def consultar_ra():
    nome = request.form['nome']
    
    aluno = db_session.query(Aluno).filter_by(nome=nome).first()
    
    if aluno:
        mensagem_recuperacao = f"O RA do aluno {aluno.nome} é {aluno.ra}."
    else:
        mensagem_recuperacao = "Aluno não encontrado. Verifique se o nome foi digitado corretamente."
    
    return render_template('index.html', mensagem_recuperacao=mensagem_recuperacao)


@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

@app.route('/DiarioDeBordo')
def DiarioDeBordo():
    # Verifique se os dados estão na sessão
    if 'ra' in session and 'nome' in session:
        ra = session['ra']
        nome = session['nome']
        
        # Passe os dados para o template
        return render_template('diario.html', ra=ra, nome=nome)


@app.route('/DiarioDeBordoInsert', methods=['POST']) 
def DiarioDeBordoInsert():
    texto = request.form.get('texto')
    acao = request.form.get('acao')
    idioma = 'pt'
    ra = session['ra']
    fk_aluno_ra = ra
    submission_time = datetime.now()
    
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

        if acao  == 'gerar_audio_e_salvar':
                novo_diario = DiarioBordo(texto=texto, fk_aluno_ra=fk_aluno_ra, datahora=submission_time)

                try:
                    db_session.add(novo_diario)  # Use db_session para adicionar
                    db_session.commit()
                except Exception as e:
                    db_session.rollback()  # Corrigido o rollback
                    print(f"Erro ao salvar no banco de dados: {e}")
                    return str(e), 500  

                                                    
        # Define o caminho do arquivo de áudio para o template
        audio_path = url_for('static', filename=audio_filename)

        return render_template('diario.html', audio_path=audio_path)

    except Exception as e:
        return str(e), 500  # Retorna erro 500 em caso de exceção


app.run(debug=True)