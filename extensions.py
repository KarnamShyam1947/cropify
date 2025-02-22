from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
