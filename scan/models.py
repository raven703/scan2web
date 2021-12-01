from app import db
from datetime import datetime


class UserDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=True)
    alliance = db.Column(db.String(64), index=True, unique=False)
    a_ticker = db.Column(db.String(64), index=True, unique=False)
    a_id = db.Column(db.String(64), index=True, unique=False)
    corporation = db.Column(db.String(64), index=True, unique=False)
    c_ticker = db.Column(db.String(64), index=True, unique=False)
    c_id = db.Column(db.String(64), index=True, unique=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
