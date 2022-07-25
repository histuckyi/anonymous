from error.exception import BadRequestError


def checkKeyInData(key, data):
    try:
        data[key]
    except Exception as e:
        raise BadRequestError
    return data[key]

