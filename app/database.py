from importacoes import *

user = 'root'
password = urllib.parse.quote_plus('andre123')
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

