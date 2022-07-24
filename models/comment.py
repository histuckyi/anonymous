from datetime import datetime
from util.serializer import Serializer

from .post import db


class Comment(db.Model, Serializer):
    __table_name__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id', ondelete='CASCADE'), nullable=True)
    content = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    # post에서 자신의 comment를 찾기 위해 설정
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f"Comment('{self.id}', '{self.content}')>"

    def serialize(self):
        d = Serializer.serialize(self)
        d['created_at'] = d['created_at'].strftime('%Y-%m-%d')
        return d
