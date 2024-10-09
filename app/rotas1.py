from flask import Blueprint
from importacoes import *
from database import db_session

rotas1 = Blueprint('rotas1', __name__)

@rotas1.route('/')
def index():
    return render_template('index.html')

@rotas1.route('/cadastro')
def cadastrar_aluno():
    return render_template('novoaluno.html')

@rotas1.route('/diario')
def abirdiario():
    return render_template('dirariobordo.html')

@rotas1.route('/logar', methods=['POST'])
def logar():
    ra = request.form['ra']
    aluno = db_session.query(Aluno).filter_by(ra=ra).first()
    
    if aluno:
        session['ra'] = aluno.ra
        session['nome'] = aluno.nome
        
        return redirect(url_for('rotas1.menu'))
    else:
        mensagem = "RA INVÁLIDA"
        return render_template('index.html', mensagem=mensagem)
    
# Rota da página do diário de bordo
@rotas1.route('/menu')
def menu():
    if 'ra' in session and 'nome' in session:
        ra = session['ra']
        nome = session['nome']
        return render_template('menu.html', ra=ra, nome=nome)
    else:
        flash('Por favor, faça login primeiro.')
        return redirect(url_for('index'))
    
@rotas1.route('/criaraluno', methods=['POST'])
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


@rotas1.route('/alunos', methods=['GET'])
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

@rotas1.route('/consultar_ra', methods=['POST'])
def consultar_ra():
    nome = request.form['nome']
    
    aluno = db_session.query(Aluno).filter_by(nome=nome).first()
    
    if aluno:
        mensagem_recuperacao = f"O RA do aluno {aluno.nome} é {aluno.ra}."
    else:
        mensagem_recuperacao = "Aluno não encontrado. Verifique se o nome foi digitado corretamente."
    
    return render_template('index.html', mensagem_recuperacao=mensagem_recuperacao)


@rotas1.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

@rotas1.route('/DiarioDeBordo')
def DiarioDeBordo():
    # Verifique se os dados estão na sessão
    if 'ra' in session and 'nome' in session:
        ra = session['ra']
        nome = session['nome']
        
        # Passe os dados para o template
        return render_template('diario.html', ra=ra, nome=nome)


@rotas1.route('/DiarioDeBordoInsert', methods=['POST']) 
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

        translator = Translator()
        texto_traduzido = translator.translate(texto, dest='en').text
        blob = TextBlob(texto_traduzido)
    
        polaridade = blob.sentiment.polarity

        if polaridade > 0:
            polaridade = "Positiva"
        elif polaridade == 0:
            polaridade = "Neutra"
        else:
            polaridade = "Negativa"

        # Salva o arquivo de áudio
        tts.save(audio_full_path)

        # Define o caminho do arquivo de áudio para o template
        audio_path = url_for('static', filename=audio_filename)

        if acao == 'gerar_audio_e_salvar':
            novo_diario = DiarioBordo(texto=texto, fk_aluno_ra=fk_aluno_ra, polaridade=polaridade)

            try:
                db_session.add(novo_diario)
                db_session.commit()
            except Exception as e:
                db_session.rollback()  
                print(f"Erro ao salvar no banco de dados: {e}")
                return str(e), 500  
        else:
            return render_template('diario.html', audio_path=audio_path)
                                                     
        return render_template('diario.html', audio_path=audio_path)

    except Exception as e:
        print(f"Erro ao processar: {e}")
        return str(e), 500
