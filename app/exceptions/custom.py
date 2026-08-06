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

class DuplicateEmailError(AppException):
    status_code = 409
    detail = "Email already in use."

class AlertNotFoundError(AppException):
    status_code = 404
    detail = "Alert not found."