from flask import Flask
from flask import Blueprint


web = Blueprint('web', __name__, static_folder='static', template_folder='templates')

@web.route('/')
def index():
    return 'Hello, World!'


app = Flask(__name__)
app.register_blueprint(web)

app.run(host='0.0.0.0', port=5000, debug=True)
