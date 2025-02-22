from flask import Flask
from extensions import db, mail, bcrypt

app = Flask(__name__)
app.config.from_prefixed_env()

db.init_app(app)
mail.init_app(app)
bcrypt.init_app(app)

from Apps.main import main
from Apps.auth import auth
from Apps.crop import crop
from Apps.shop import shop
from Apps.query import query
from Api.api import api

app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(crop)
app.register_blueprint(shop)
app.register_blueprint(query)
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
