from flask import request
from flask_restx import Resource, Namespace
from sqlalchemy import exc

from error import exception
from error.exception import BaseError, BadRequestError
from models.post import Post as PostModel
from query import basic_query, post_query
from service.notification import notify
from util.api_exception_response import ApiExceptionResponse

Post = Namespace("Post")


@Post.route('')
class BoardPosts(Resource):

    def get(self):
        size = int(request.args.get('size', 10))
        page = int(request.args.get('page', 1))
        result = basic_query.paginate(PostModel, page, size)
        return {
            "total": result.total,
            "page": result.page,
            "per_page": result.per_page,
            "has_next": result.has_next,
            "posts": PostModel.serialize_list(result.items)
        }

    def post(self):
        data = request.get_json()
        name = data['name']
        if post_query.existName(name):
            raise exception.DuplicatedNameError

        title = data['title']
        content = data['content']
        password = data['password']
        try:
            new_post = basic_query.insert(PostModel, name=name, title=title, content=content, password=password)
        except exc.IntegrityError:
            raise exception.BadRequestError
        result = PostModel.serialize(new_post)
        notify(content)
        return 200


@Post.route('/<int:post_id>')
class BoardPost(Resource):

    def put(self, post_id):
        post = basic_query.get(PostModel, id=post_id)
        data = request.get_json()
        if 'password' not in data and data['password']:
            raise BadRequestError
        password = data['password']
        post.title = data['title']
        basic_query.update(PostModel, post_id, author=data['author'], title=data['title'], content=data['content'])

    def delete(self, post_id):
        post = basic_query.get(PostModel, id=post_id)
        data = request.get_json()
        if 'password' not in data and data['password']:
            raise BadRequestError
        password = data['password']
        basic_query.delete(PostModel, post_id)


@Post.errorhandler(BaseError)
def post_error_handler(error):
    return ApiExceptionResponse(error).response()
