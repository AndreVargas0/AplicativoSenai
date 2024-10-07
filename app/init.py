from importacoes import * 
from rotas1 import rotas1  
from rotas2 import rotas2 
                                                                                                                                                                                                                                                                                                                                                            

app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = 'session_flask'
app.secret_key = '1234'

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
DiarioBordo = Base.classes.diariobordo

Session = sessionmaker(bind=engine)
db_session = Session()


app.register_blueprint(rotas1)
app.register_blueprint(rotas2)


app.run(debug=True)
