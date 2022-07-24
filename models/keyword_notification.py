from datetime import datetime
from util.serializer import Serializer

from .post import db


class KeywordNotification(db.Model, Serializer):
    __table_name__ = 'keyword_notification'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keyword = db.Column(db.String(300), nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<KeywordNotification('{self.name}', '{self.keyword}')>"

    def serialize(self):
        d = Serializer.serialize(self)
        del d['created_at']
        del d['keyword']
        del d['id']
        return d
