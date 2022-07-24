from error.exception import BaseError


class ApiExceptionResponse:
    def __init__(self, exception: BaseError):
        self.exception = exception

    def response(self):
        return {
            'status_code': self.exception.status,
            "code": self.exception.code,
            "message": self.exception.message
        }, self.exception.status
