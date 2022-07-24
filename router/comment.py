from flask import request, Response
from flask_restx import Resource, Namespace
from flask_sqlalchemy import BaseQuery

from error.exception import BadRequestError
from models.keyword_notification import KeywordNotification as KeywordNotiModel
from query import comment_query, keyword_noti_query
from query import basic_query
from models.comment import Comment as CommentModel
from models.post import Post as PostModel
from service.notification import notify
from util.keyword_analyzer import KeywordAnalyzer

Comment = Namespace("Comment")


@Comment.route('/<int:post_id>')
class Comments(Resource):

    def get(self, post_id):
        comments = comment_query.get_filter_by_post_id(post_id)
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
            basic_query.get(PostModel, post_id)
            if 'parent_comment_id' in data and data['parent_comment_id']:
                basic_query.get(CommentModel, parent_comment_id)
            basic_query.insert(CommentModel, post_id=post_id, content=content, parent_comment_id=parent_comment_id)
        except Exception as e:
            print(e)
            raise BadRequestError
        # comment 키워드를 추출하고, 키워드를 등록한 유저에게 알람
        notify(content)
        return 201

