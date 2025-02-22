from datetime import datetime
from App import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    role = db.Column(db.String(20))
    email = db.Column(db.String(30))
    password = db.Column(db.String(255))
    isVerified = db.Column(db.Integer)
    products = db.relationship("ProductModel", backref = 'users', cascade='all, delete')
    queries = db.relationship("QueryModel", backref = 'users', cascade='all, delete')
    orders = db.relationship("OrderModel", backref = 'users', cascade='all, delete')

    def __repr__(self):
        return "<User " + self.name + ">"
    
class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(30))
    price = db.Column(db.Integer)
    img_url = db.Column(db.String(30))
    userId = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return "<Product " + self.name + ">"
    
class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    productId=db.Column(db.Integer, db.ForeignKey('products.id'))
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    time = db.Column(db.DateTime, default=datetime.now)

class QueryModel(db.Model):
    __tablename__ = "queries"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(30))
    time = db.Column(db.DateTime, default=datetime.now)
    img_url = db.Column(db.String(30))
    userId = db.Column(db.Integer, db.ForeignKey("users.id"))
    answers = db.relationship("AnswerModel", backref = 'queries', cascade='all, delete')

class AnswerModel(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(300))
    name = db.Column(db.String(30))
    time = db.Column(db.DateTime, default=datetime.now)
    qid = db.Column(db.Integer, db.ForeignKey("queries.id"))
