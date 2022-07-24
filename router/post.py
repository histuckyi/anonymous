from flask import request
from flask_restx import Api, Resource, Namespace

from error import exception
from error.exception import BaseError
from models.post import Post as PostModel
from query import basicQuery, postQuery
from sqlalchemy import exc

from util.APIExceptionResponse import ApiExceptionResponse

Post = Namespace("Post")


@Post.route('')
class BoardPosts(Resource):

    def get(self):
        size = int(request.args.get('size', 10))
        page = int(request.args.get('page', 3))
        result = basicQuery.paginate(PostModel, page, size)
        return {"total": result.total, "posts": PostModel.serialize_list(result.items)}

    def post(self):
        data = request.get_json()
        name = data['name']
        if postQuery.existName(name):
            raise exception.DuplicatedNameError

        title = data['title']
        content = data['content']
        password = data['password']
        try:
            new_post = basicQuery.insert(PostModel, name=name, title=title, content=content, password=password)
        except exc.IntegrityError:
            raise exception.BadRequestError
        result = PostModel.serialize(new_post)
        return 200


@Post.route('/<int:post_id>')
class BoardPost(Resource):

    def put(self, post_id):
        post = basicQuery.get(PostModel, id=post_id)
        data = request.get_json()
        post.password = data['password']
        post.title = data['title']
        basicQuery.update(PostModel, post_id, author=data['author'], title=data['title'], content=data['content'])

    def delete(self, post_id):
        post = basicQuery.get(PostModel, id=post_id)
        data = request.get_json()
        post.password = data['password']
        basicQuery.delete(PostModel, post_id)


@Post.errorhandler(BaseError)
def post_error_handler(error):
    return ApiExceptionResponse(error).response()