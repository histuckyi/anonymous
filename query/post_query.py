from models.post import Post


def existName(name):
    return Post.query.filter(Post.name == name).count() > 0


def paginateWithTitle(model, page, size, title):
    return model.query.filter(Post.title.like(f'%{title}%')).paginate(page=page, per_page=size, error_out=True)


def paginateWithName(model, page, size, name):
    return model.query.filter(Post.name.like(f'%{name}%')).paginate(page=page, per_page=size, error_out=True)
