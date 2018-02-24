from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)

####### Configurations ###########################
app.config['SECRET_KEY'] = 'rajas-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:dinkan124!@localhost/movierec'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
####### Configurations - end ######################

Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models