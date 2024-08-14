from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/novoaluno')
def cadastrar_aluno():
    return render_template('novoaluno.html')

@app.route('/diario')
def logar():
    return render_template('dirariobordo.html')

@app.route('/diario',methods=['post'])
def abirdiario():
    ra = request.form('ra')
    if ra == 12345619:
        return render_template('diariobordo.html')
    else:
        return f'O ra está errado'
app.run(debug=True)



#AMOALANAS2S2