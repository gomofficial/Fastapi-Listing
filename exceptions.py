from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException, status

class UserNotFoundError(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail="User not found"

class UserAlreadyExists(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail="User already exists"

class UsernameAlreadyExists(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail="Username already exists"

class EmailAlreadyExists(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail="Email already exists"

class UserAuthenticationError(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail="wrong username or password"

class ListingNotFoundError(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail="404 not found"

class InvalidPermission(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail="you dont have permission"

class RateLimitException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_429_TOO_MANY_REQUESTS
        self.detail="Too Many Requests"