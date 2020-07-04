from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Client(db.Model):
    __tablename__ = "Client"
    id = db.Column(db.Integer, primary_key = True)
    client_id = db.Column(db.Integer, nullable = False)
    deal_id = db.Column(db.Integer, nullable = False)
    client_name = db.Column(db.String, nullable = False)
    deal_name = db.Column(db.String, nullable = False)
    date= db.Column(db.String, nullable = False)
    accepted = db.Column(db.Integer, nullable = False)
    refused = db.Column(db.Integer, nullable = False)

     



