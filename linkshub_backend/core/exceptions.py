from rest_framework import status


class CustomValidationError(Exception):
    def __init__(self, message, code, status_code=status.HTTP_400_BAD_REQUEST, errors=None, data=None, success=None):
        self.success = success
        self.message = message
        self.code = code
        self.status_code = status_code
        self.errors = errors or []
        self.data = data or {}
        super().__init__(self.message)

    def to_dict(self):
        return {
            "success": self.success,
            "message": self.message,
            "code": self.code,
            'status_code': self.status_code,
            "errors": self.errors or [],
            'data': self.data or {}
        }
