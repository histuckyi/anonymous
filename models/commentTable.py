from models.comment import Comment


def getFilter(value):
    data = Comment.query.filter(Comment.post_id == value).order_by(Comment.created_at.asc()).all()
    return data