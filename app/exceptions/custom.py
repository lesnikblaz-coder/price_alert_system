from app.exceptions.base import AppException


class InvalidTokenError(AppException):
    status_code = 401
    detail = "Invalid token."

class InvalidCredentialsError(AppException):
    status_code = 401
    detail = "Invalid authentication credentials."

class UserNotFoundError(AppException):
    status_code = 404
    detail = "User not found."