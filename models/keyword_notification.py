from datetime import datetime
from util.serializer import Serializer

from .post import db


class KeywordNotification(db.Model, Serializer):
    __table_name__ = 'keyword_notification'

    keyword = db.Column(db.String(300), nullable=False),
    name = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<KeywordNotification('{self.name}', '{self.keyword}')>"
