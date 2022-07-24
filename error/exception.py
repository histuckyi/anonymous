class BaseError(Exception):
    def __init__(self, code='POST00', status=400, message='unexpected Exception', params=[], error_message=''):
        Exception.__init__(self)
        self.code = code
        self.status = status
        self.message = message
        self.params = params
        self.error_message = error_message
        # self.logger = log.logger

    def __str__(self):
        return self.message

    def to_dict(self):
        response = {'code': self.code, 'status': self.status, 'message': self.message}
        return response


class BadRequestError(BaseError):
    def __init__(self):
        BaseError.__init__(self)
        self.code = "POST001"
        self.status = 400
        self.message = '요청에 필요한 파라미터 값이 존재하지 않거나 올바르지 않은 파라미터 값이 포함되었습니다'


class DuplicatedNameError(BaseError):
    def __init__(self):
        BaseError.__init__(self)
        self.code = "POST002"
        self.status = 400
        self.message = '중복된 이름으로 요청하셨습니다.'
