import json

from flask import request, jsonify
from flask_restx import Api, Resource, Namespace
from models.post import Post as PostModel
from models import database

Post = Namespace("Post")


@Post.route('')
class BoardPosts(Resource):

    def get(self):
        size = int(request.args.get('size', 10))
        page = int(request.args.get('page', 3))
        result = database.paginate(PostModel, page, size)
        return {"total": result.total, "posts": PostModel.serialize_list(result.items)}

    def post(self):
        data = request.get_json()
        author = data['author']
        title = data['title']
        content = data['content']
        password = data['password']
        database.insert(PostModel, author=author, title=title, content=content, password=password)
        return json.dumps("Added"), 200


@Post.route('/<int:post_id>')
class BoardPost(Resource):

    def put(self, post_id):
        post = database.get(PostModel, id=post_id)
        data = request.get_json()
        post.password = data['password']
        post.title = data['title']
        database.update(PostModel, post_id, author=data['author'], title=data['title'], content=data['content'])

    def delete(self, post_id):
        post = database.get(PostModel, id=post_id)
        data = request.get_json()
        post.password = data['password']
        database.delete(PostModel, post_id)

