from flask import request
from flask_restx import Resource, Namespace

from error.exception import BadRequestError
from models.comment import Comment as CommentModel
from models.post import Post as PostModel
from query import basic_query
from query import comment_query
from service.notification import notify

Comment = Namespace("Comment")


@Comment.route('/<int:post_id>')
class Comments(Resource):

    def get(self, post_id):
        size = int(request.args.get('size', 10))
        page = int(request.args.get('page', 1))
        sub_size = int(request.args.get('sub_size', 10))
        sub_page = int(request.args.get('sub_page', 1))

        main_comments = comment_query.get_filter_by_post_id(post_id, sub_size, sub_page)
        result = {
            "total": main_comments.total,
            "page": main_comments.page,
            "per_page": main_comments.per_page,
            "has_next": main_comments.has_next,
            "comments": []
        }
        for comment in main_comments.items:
            comment = CommentModel.serialize(comment)
            parent = {
                'id': comment['id'],
                'content': comment['content'],
                'created_at': comment['created_at'],
                'is_parent': True
            }

            sub_comments = comment_query.pagination_by_post_id_and_parent_comment_id(post_id, comment['id'], size,
                                                                                     page)
            child = {
                'total': sub_comments.total,
                'page': sub_comments.page,
                'per_page': sub_comments.per_page,
                'has_next': sub_comments.has_next,
                'sub_comments' : []

            }
            for sub_comment in sub_comments.items:
                sub_comment = CommentModel.serialize(sub_comment)
                child['sub_comments'].append({
                    'id': sub_comment['id'],
                    'content': sub_comment['content'],
                    'created_at': sub_comment['created_at'],
                    'parent_comment_id': sub_comment['parent_comment_id'],
                    'is_parent': False
                }
                )
            parent['child'] = child
        result['comments'].append(parent)
        return result, 200

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
