from flask import Blueprint
from importacoes import * 
from init import db_session

rotas2 = Blueprint('rotas2', __name__)

@rotas2.route('/logar_soe', methods=['POST'])
def logar():
    db_session = Session()
    rg = request.form['rg']
    Soe = db_session.query(funcionario).filter_by(rg=rg).first()
    
    if funcionario:
        session['rg'] = funcionario.rg
        session['nome'] = funcionario.nome
        
        return redirect(url_for('menu_soe'))
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
    
@rotas2.route('/sentimentosalunos')
def sentimentosalunos():
    # Consultar os dados
    query = db.session.query(DiarioBordo.polaridade).all()
    df = pd.DataFrame(query, columns=['polaridade'])

    # Contar os valores
    count_df = df['polaridade'].value_counts().reset_index()
    count_df.columns = ['polaridade', 'count']

    return render_template('sentimentos_alunos.html', data=count_df.to_dict(orient='records'))
    
@rotas2.route('/grafico')
def grafico():
    # Reutilizar a consulta
    query = db.session.query(DiarioBordo.polaridade).all()
    df = pd.DataFrame(query, columns=['polaridade'])
    count_df = df['polaridade'].value_counts().reset_index()
    count_df.columns = ['polaridade', 'count']

    # Criar o gráfico
    plt.figure(figsize=(8, 6))
    sns.barplot(x='polaridade', y='count', data=count_df)
    plt.title('Distribuição de Polaridade')
    plt.xlabel('Polaridade')
    plt.ylabel('Contagem')
    
    # Salvar o gráfico
    graph_path = os.path.join('static', 'grafico.png')
    plt.savefig(graph_path)
    plt.close()

    return render_template('grafico.html', graph_path=graph_path)