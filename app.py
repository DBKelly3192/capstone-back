from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import current_user, login_required, LoginManager
from flask_mail import Mail, Message
from resources.posts import post
from resources.users import user
from playhouse.shortcuts import model_to_dict
import os
import models

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.config.update(
  SESSION_COOKIE_SECURE=True,
  SESSION_COOKIE_SAMESITE='None'
)
app.secret_key = "What happens in a meadow at dusk?"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        user = models.User.get_by_id(user_id)
        return user
    except models.DoesNotExist:
        return None

CORS(post, origins=['http://localhost:3000', 'https://happy-trails-back.herokuapp.com'], supports_credentials = True)
CORS(user, origins=['http://localhost:3000', 'https://happy-trails-back.herokuapp.com'], supports_credentials = True)

app.register_blueprint(post, url_prefix='/posts')
app.register_blueprint(user, url_prefix='/users')

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
