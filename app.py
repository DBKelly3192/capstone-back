from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import current_user, login_required, LoginManager
from flask_mail import Mail, Message
from playhouse.shortcuts import model_to_dict
from resources.posts import post
from resources.users import user
from resources.sos import sos
import models
import os

DEBUG = True
PORT = 8000

app = Flask(__name__)

if 'ON_HEROKU' in os.environ:
    app.config.update(
      SESSION_COOKIE_SECURE=True,
      SESSION_COOKIE_SAMESITE='None'
    )

app.secret_key = "What happens in a meadow at dusk?"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'Happy.Trails.SOS@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'Happy.Trails.SOS@gmail.com'
app.config['MAIL_PASSWORD'] = 'nosbec-Xongum-3gexsi'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        user = models.User.get_by_id(user_id)
        return user
    except models.DoesNotExist:
        return None

CORS(post, origins=['http://localhost:3000', 'https://happy-trails-app.herokuapp.com'], supports_credentials = True)
CORS(user, origins=['http://localhost:3000', 'https://happy-trails-app.herokuapp.com'], supports_credentials = True)
CORS(sos, origins=['http://localhost:3000', 'https://happy-trails-app.herokuapp.com'], supports_credentials = True)

mail = Mail(app)

@app.route("/email/send")
def index():
    msg = Message(
        "Your friend hasn't checked in!",
        recipients = ["DavidBenjaminKelly@gmail.com"]
    )
    msg.body = "Keep your cool. The first step is to establish contact with your friend. Call, text, or visit their home/place of business. If you cannot reach your friend through these methods, you should consider reaching out to local law enforcement."
    mail.send(msg)
    return jsonify(
        data={},
        status={ "code": 201, "message": "success" }
    )

app.register_blueprint(post, url_prefix='/posts')
app.register_blueprint(user, url_prefix='/users')
app.register_blueprint(sos, url_prefix='/sos')

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

if 'ON_HEROKU' in os.environ:
    print('/non heroku!')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
