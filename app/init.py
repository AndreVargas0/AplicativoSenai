from database import *
from rotas1 import *
from rotas2 import *

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'session_flask'
app.secret_key = '1234'

app.register_blueprint(rotas1)
app.register_blueprint(rotas2)

app.run(debug=True)
