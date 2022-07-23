from flask import request, jsonify
from flask_restx import Api, Resource, Namespace

Comment = Namespace("Comment")


@Comment.route('')
class Comments(Resource):

    def get(self):
        return jsonify({"hello": "world"})
