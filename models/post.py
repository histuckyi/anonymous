from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from util.serializer import Serializer

db = SQLAlchemy()


class Post(db.Model, Serializer):
    __table_name__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Post('{self.id}', '{self.title}')>"

    def serialize(self):
        d = Serializer.serialize(self)
        del d['password']
        del d['comments']
        d['created_at'] = d['created_at'].strftime('%Y-%m-%d')
        return d

