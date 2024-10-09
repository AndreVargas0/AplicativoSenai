from flask import Blueprint
from importacoes import * 
from database import db_session

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
    ra = request.args.get('ra') 
    polaridade_desejada = request.args.get('polaridade')  # Captura a polaridade selecionada

    # Faz o join entre Aluno e DiarioBordo para obter a polaridade e o nome do aluno com base no RA
    query = (
        db_session.query(Aluno.nome, DiarioBordo.polaridade, DiarioBordo.texto)
        .join(DiarioBordo, Aluno.ra == DiarioBordo.fk_aluno_ra)
        .filter(Aluno.ra == ra)
        .all()
    )

    if not query:
        return "Nenhum dado encontrado para o aluno selecionado.", 404

    # Criar DataFrame a partir da consulta
    df = pd.DataFrame(query, columns=['nome', 'polaridade', 'texto'])

    # Contar a polaridade
    count_df = df['polaridade'].value_counts().reset_index()
    count_df.columns = ['polaridade', 'count']

    # Obter o nome do aluno
    aluno_nome = df['nome'].iloc[0]  # Pega o nome do aluno da primeira linha

    # Criar o gráfico de polaridade
    plt.figure(figsize=(8, 6))
    sns.barplot(x='polaridade', y='count', data=count_df)
    plt.title(f'Distribuição de Polaridade para o Aluno {aluno_nome}')
    plt.ylabel('Contagem')
    
    # Salvar o gráfico de polaridade
    base_dir = os.path.abspath(os.path.dirname(__file__))
    static_dir = os.path.join(base_dir, 'static')

    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    grafico_filename = f'grafico_{ra}.png'
    graph_path = os.path.join(static_dir, grafico_filename)
    
    plt.savefig(graph_path)
    plt.close()

    # Gerar nuvem de palavras com filtro de polaridade
    if polaridade_desejada:
        df_filtrado = df[df['polaridade'] == polaridade_desejada]
        
        print(f'Polaridade desejada: {polaridade_desejada}')  # Log da polaridade desejada
        print(f'Dados filtrados: {df_filtrado}')  # Log dos dados filtrados

        # Verifique se existem textos filtrados antes de gerar a nuvem de palavras
        if not df_filtrado.empty:
            texto_combined = " ".join(df_filtrado['texto'])
            stopwords = set(STOPWORDS)

            wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(texto_combined)

            # Salvar a nuvem de palavras
            nuvem_filename = f'nuvem_palavras_{ra}.png'
            nuvem_path = os.path.join(static_dir, nuvem_filename)
            wordcloud.to_file(nuvem_path)
            print(f'Nuvem de palavras salva em: {nuvem_path}')  # Log do caminho salvo
        else:
            print('Nenhum texto disponível para a nuvem de palavras.')  # Log se não houver textos
            nuvem_path = None  # Não gera nuvem de palavras se não houver textos
    else:
        nuvem_path = None  # Se não houver polaridade desejada, não gera nuvem de palavras
    
    rg = session['rg']
    alunos = db_session.query(Aluno).all()
    nome = session['nome']
    return render_template('graficos_alunos.html', graph_path=f'/static/{grafico_filename}', nuvem_path=f'/static/{nuvem_filename}', nome=nome, alunos=alunos,rg=rg)


@rotas2.route('/menu_soe')
def listadrop():
    alunos = db_session.query(Aluno).all()
    nome = session['nome']
    rg= session['rg']
    return render_template('graficos_alunos.html', alunos=alunos, nome=nome,rg=rg)