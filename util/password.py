import bcrypt


# 암호화
from error.exception import BadRequestError


def encryption(password):
    bytes_hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return bytes_hashed_password.decode('utf-8')


# 입력된 패스워드를 DB 값과 확인
def matches(bytes_hashed_password, input_password):
    if not bcrypt.checkpw(input_password.encode('utf-8'), bytes_hashed_password.encode('utf-8')):
        raise BadRequestError
    return True
