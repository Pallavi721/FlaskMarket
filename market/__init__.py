from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# __name__ is a magic method that refers to the current file
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'b4614831e2df2fc5315b24ef'
db = SQLAlchemy(app)

# bcrypt generates hash passwords
bcrypt = Bcrypt(app)

# means you are creating a LoginManager instance and linking it to your Flask app.
login_manager = LoginManager(app)
# it redirects the non-logged-in user to the login_page
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

from market import routes