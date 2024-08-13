from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/novoaluno')
def cadastrar_aluno():
    return render_template('novoaluno.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

app.run(debug=True)
