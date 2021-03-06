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


class ShipDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(64), index=True, unique=False)
    url = db.Column(db.String(64), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class InvTypes(db.Model):

    typeid = db.Column(db.Integer, primary_key=True)
    groupid = db.Column(db.String(64), index=True, unique=False)
    typename = db.Column(db.String(64), index=True, unique=False)

