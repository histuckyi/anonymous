from flask import request, Response
from flask_restx import Resource, Namespace

from query import commentQuery
from query import basicQuery
from models.comment import Comment as CommentModel
from models.post import Post as PostModel

Comment = Namespace("Comment")


@Comment.route('/<int:post_id>')
class Comments(Resource):

    def get(self, post_id):
        comments = commentQuery.get_filter_by_post_id(post_id)
        comments = CommentModel.serialize_list(comments)
        result = {}
        for comment in comments:
            if comment['parent_comment_id'] is None:
                result[comment['id']] = {
                    'id': comment['id'],
                    'content': comment['content'],
                    'created_at': comment['created_at'],
                    'is_parent': True,
                    'sub_comments': []
                }
            else:
                result[comment['parent_comment_id']]['sub_comments'].append({
                    'id': comment['id'],
                    'content': comment['content'],
                    'created_at': comment['created_at'],
                    'parent_comment_id': comment['parent_comment_id'],
                    'is_parent': False
                }
                )
        return list(result.values()), 200

    def post(self, post_id):
        data = request.get_json()
        if 'content' not in data:
            raise BaseException

        content = data['content']
        parent_comment_id = data['parent_comment_id']
        try:
            post = basicQuery.get(PostModel, post_id)
            if 'parent_comment_id' in data:
                basicQuery.get(CommentModel, parent_comment_id)
        except PostModel.DoesNotExist:
            raise BaseException
        basicQuery.insert(CommentModel, post_id=post_id, content=content, parent_comment_id=parent_comment_id)
        return Response(status=201)
