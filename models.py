from datetime import datetime

from cam import db


class Orders(db.Model):
    order_id = db.Column(db.String(8), primary_key=True, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    complete = db.Column(db.Boolean, default=False, nullable=False)


class Images(db.Model):
    image_id = db.Column(db.String(8), nullable=False, primary_key=True)
    order_id = db.Column(db.String(8), db.ForeignKey("orders.order_id"), nullable=False)
