from flask import Blueprint
from importacoes import * 
from database import db_session
matplotlib.use('Agg')
rotas2 = Blueprint('rotas2', __name__)

@rotas2.route('/logar_soe', methods=['POST'])
def logar():
    rg = request.form['ra']
    funcionario = db_session.query(Funcionario).filter_by(rg=rg).first()
    
    if funcionario:
        session['rg'] = funcionario.rg
        session['nome'] = funcionario.nome
        
        return redirect(url_for('rotas2.menu_soe'))
    else:
        mensagem = "RA INVÁLIDA"
        return render_template('index.html', mensagem=mensagem)

@rotas2.route('/Menu_soe')
def menu_soe():
    if 'rg' in session and 'nome' in session:
        rg = session['rg']
        nome = session['nome']
        return render_template('menu_soe.html', rg=rg, nome=nome)
    else:
        flash('Por favor, faça login primeiro.')
        return redirect(url_for('index'))
    
    

@rotas2.route('/grafico')
def grafico():
    ra = request.args.get('ra')  # Traz o ra que está linkado com o nome 
    polaridade_desejada = request.args.get('polaridade')  # Captura a polaridade selecionada

    # Faz o join entre Aluno e DiarioBordo para obter a polaridade e o nome do aluno com base no RA
    query = (
        db_session.query(Aluno.nome, DiarioBordo.datahora, DiarioBordo.polaridade, DiarioBordo.texto)
        .join(DiarioBordo, Aluno.ra == DiarioBordo.fk_aluno_ra)
        .filter(Aluno.ra == ra)
        .all()
    )

    if not query:
        return "Nenhum dado encontrado para o aluno selecionado.", 404

    # Cria um DataFrame
    df = pd.DataFrame(query, columns=['nome', 'datahora', 'polaridade', 'texto'])

    # Contar a polaridade - Positiva, Neutra, Negativa
    count_df = df['polaridade'].value_counts().reset_index()
    count_df.columns = ['polaridade', 'count']

    # Obter o nome do aluno para o gráfico
    aluno_nome = df['nome'].iloc[0]

    # Criar o gráfico de polaridade
    plt.figure(figsize=(8, 6))
    sns.barplot(x='polaridade', y='count', data=count_df)
    plt.title(f'Distribuição de Polaridade para o Aluno {aluno_nome}')
    plt.ylabel('Contagem')

    # Criar a pasta 'graficos' dentro de 'static' se não existir
    graficos_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'graficos')
    os.makedirs(graficos_dir, exist_ok=True)

    grafico_filename = 'grafico_polaridade.png'  # Nome fixo
    graph_path = os.path.join(graficos_dir, grafico_filename)
    
    plt.savefig(graph_path)
    plt.close()

    # Gerar nuvem de palavras com filtro de qual polaridade
    if polaridade_desejada:
        df_filtrado = df[df['polaridade'] == polaridade_desejada]

        if not df_filtrado.empty:
            texto_combined = " ".join(df_filtrado['texto'])
            stopwords = set(STOPWORDS)

            wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(texto_combined)

            # Criar a figura para a nuvem de palavras
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')  # Desliga os eixos
            plt.title(f'Nuvem de palavras da polaridade {polaridade_desejada} do aluno(a) {aluno_nome}', fontsize=20)

            # Salvar a nuvem de palavras dentro da pasta 'graficos'
            nuvem_filename = 'nuvem_palavras.png'  # Nome fixo
            nuvem_path = os.path.join(graficos_dir, nuvem_filename)
            plt.savefig(nuvem_path, bbox_inches='tight')
            plt.close()
        else:
            nuvem_path = None
    else:
        nuvem_path = None

    # Gerar gráfico de linha para polaridade negativa
    df_negativa = df[df['polaridade'] == 'Negativa']

    if not df_negativa.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(df_negativa['datahora'], df_negativa['polaridade'], marker='o')
        plt.title(f'Polaridade Negativa ao Longo do Tempo para {aluno_nome}')
        plt.xlabel('Data e Hora')
        plt.ylabel('Polaridade')
        plt.xticks(rotation=45)
        plt.grid()

        # Salvar o gráfico de polaridade negativa dentro da pasta 'graficos'
        grafico_negativo_filename = 'grafico_negativo.png'  # Nome fixo
        graph_negativo_path = os.path.join(graficos_dir, grafico_negativo_filename)
        plt.savefig(graph_negativo_path)
        plt.close()
    else:
        graph_negativo_path = None

    rg = session['rg']
    alunos = db_session.query(Aluno).all()
    nome = session['nome']
    session['aluno_nome'] = aluno_nome

    return render_template('graficos_alunos.html', 
                           graph_path='/static/graficos/grafico_polaridade.png', 
                           nuvem_path='/static/graficos/nuvem_palavras.png', 
                           graph_negativo_path='/static/graficos/grafico_negativo.png', 
                           nome=nome, alunos=alunos, rg=rg)

@rotas2.route('/download_zip')
def download_zip():
    aluno_nome = session.get('aluno_nome')
    if not aluno_nome:
        return "Aluno não encontrado.", 404

    aluno_nome = aluno_nome.replace(" ", "")
    zip_filename = f'Graficos_do_aluno_{aluno_nome}'
    zip_path = os.path.join('static', zip_filename)

    # Define o diretório de gráficos a ser zipado
    folder_to_zip = os.path.join('static', 'graficos')

    # Cria o arquivo zip
    shutil.make_archive(zip_path, 'zip', folder_to_zip)

    # Retorna o arquivo zip como download
    return send_file(f'{zip_path}.zip', as_attachment=True, download_name=f'{zip_filename}.zip')


@rotas2.route('/download_zip')
def download_zip():
    # Caminho da pasta que você deseja zipar
    folder_path = os.path.join('static', 'graficos')
    zip_buffer = BytesIO()

    # Cria o arquivo ZIP
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                # Adiciona o arquivo ao ZIP
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))

    # Volta para o início do BytesIO buffer
    zip_buffer.seek(0)

    # Retorna o arquivo ZIP como resposta
    return send_file(zip_buffer, as_attachment=True, download_name='graficos.zip', mimetype='application/zip')


@rotas2.route('/menu_soe')
def listadrop():
    alunos = db_session.query(Aluno).all()
    nome = session['nome']
    rg= session['rg']
    return render_template('graficos_alunos.html', alunos=alunos, nome=nome,rg=rg)


