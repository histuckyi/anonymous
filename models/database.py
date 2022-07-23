from .post import db


def get_all(model):
    data = model.query.all()
    return data


def paginate(model, page, size):
    return model.query.paginate(page=page, per_page=size, error_out=True)


def insert(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit()


def get(model, id):
    data = model.query.filter_by(id=id)
    return data


def delete(model, id):
    model.query.filter_by(id=id).delete()
    commit()


def update(model, id, **kwargs):
    instance = model.query.filter_by(id=id).all()[0]
    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    commit()


def commit():
    db.session.commit()
