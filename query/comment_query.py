from sqlalchemy import desc, and_

from models.comment import Comment


def get_filter_by_post_id(post_id, size, page):
    return Comment.query.filter_by(post_id=post_id, parent_comment_id=None).order_by(
        desc('created_at')).paginate(page=page, per_page=size, error_out=True)


def pagination_by_post_id_and_parent_comment_id(post_id, parent_comment_id, size, page):
    return Comment.query.filter_by(post_id=post_id, parent_comment_id=parent_comment_id).order_by(
        desc('created_at')).paginate(page=page, per_page=size, error_out=True)