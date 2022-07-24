from flask_restx import Api
from app import create_app
from router.comment import Comment
from router.post import Post
from models.post import db


app = create_app()
db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()


api = Api(
    app,
    version='0.0.1',
    title="Anonymous's API Server",
    description="This project is for Wanted assignment",
    terms_url="/",
    contact="histuckyi@gmail.com",
    license="MIT"
)


api.add_namespace(Comment, '/comments')
api.add_namespace(Post, '/posts')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
