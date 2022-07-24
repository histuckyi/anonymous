from models.comment import Comment


def get_filter_by_post_id(post_id):
    return Comment.query.filter(Comment.post_id == post_id).order_by(Comment.created_at.asc()).all()
