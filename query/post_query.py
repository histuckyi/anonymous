from models.post import Post


def existName(name):
    return Post.query.filter(Post.name == name).count() > 0
