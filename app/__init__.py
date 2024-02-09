from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_url
from flask_mail import Mail



from config import Config

app=Flask(__name__)


login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_vew='login'
bcrypt=Bcrypt(app)

app.config['SECRET_KEY']="j-ITiFqDJMq2bqXLf3-DIg"
app.config.from_object(Config)

UPLOAD_FOLDER = 'app/static/Images/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'egpouli@gmail.com'
# app.config['MAIL_PASSWORD'] = 'TG-2166-AI'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///shop.db'
mail = Mail(app)
db=SQLAlchemy(app)
migrate=Migrate(app,db)



Bootstrap(app)
from app import routes