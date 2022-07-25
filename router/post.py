from flask import request, Response
from flask_restx import Resource, Namespace
from sqlalchemy import exc

from error import exception
from error.exception import BaseError, BadRequestError
from models.post import Post as PostModel
from query import basic_query, post_query
from service.notification import notify
from util.api_exception_response import ApiExceptionResponse
from util.password import matches, encryption
from util.validation import checkKeyInData

Post = Namespace("Post")


@Post.route('')
class BoardPosts(Resource):

    def get(self):
        size = int(request.args.get('size', 10))
        page = int(request.args.get('page', 1))
        title = request.args.get('title', None)
        name = request.args.get('name', None)
        if title:
            result = post_query.paginateWithTitle(PostModel, page, size, title)
        elif name:
            result = post_query.paginateWithName(PostModel, page, size, name)
        else:
            result = basic_query.paginate(PostModel, page, size)
        return {
            "total": result.total,
            "page": result.page,
            "per_page": result.per_page,
            "has_next": result.has_next,
            "posts": PostModel.serialize_list(result.items)
        }, 200

    def post(self):
        data = request.get_json()
        name = data['name']
        if post_query.existName(name):
            raise exception.DuplicatedNameError

        title = checkKeyInData('title', data)
        content = checkKeyInData('content', data)
        password = checkKeyInData('password', data)
        try:
            new_post = basic_query.insert(PostModel, name=name, title=title, content=content, password=encryption(password))
        except exc.IntegrityError:
            raise exception.BadRequestError
        notify(content)
        return Response(status=200)


@Post.route('/<int:post_id>')
class BoardPost(Resource):

    def put(self, post_id):
        post = basic_query.get(PostModel, id=post_id).first()
        data = request.get_json()
        title = checkKeyInData('title', data)
        name = checkKeyInData('name', data)
        content = checkKeyInData('content', data)
        checkKeyInData('password', data)
        matches(post.password, data['password'])
        basic_query.update(PostModel, post_id, name=name, title=title, content=content)
        return Response(status=200)

    def delete(self, post_id):
        post = basic_query.get(PostModel, id=post_id).first()
        data = request.get_json()
        checkKeyInData('password', data)
        matches(post.password, data['password'])
        basic_query.delete(PostModel, post_id)
        return Response(status=200)


@Post.errorhandler(BaseError)
def post_error_handler(error):
    return ApiExceptionResponse(error).response()
