from app import db


class Servlet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer(4))
    latest_ver = db.Column(db.String(4), index=True, unique=True)
