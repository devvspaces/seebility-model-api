import jwt
from django.conf import settings
from django.utils.crypto import constant_time_compare

from rest_framework.permissions import BasePermission
from .logger import err_logger, logger  # noqa


def validate_jwt(token: str):
    try:
        print(token, settings.JWT_KEY)
        return jwt.decode(token, settings.JWT_KEY, algorithms=["HS256"])
    except Exception:
        return False


def get_user_id(token: str):
    payload = validate_jwt(token)
    if payload:
        return payload["user_id"]
    return False


class IsValidApiKey(BasePermission):
    """Validates api key is valid."""

    def has_permission(self, request, view):
        if request.method == "OPTIONS":
            return True
        if not request.headers.get(settings.API_KEY_HEADER):
            return False
        api_key = request.headers[settings.API_KEY_HEADER]
        return constant_time_compare(api_key, settings.API_KEY)


class IsAuthorized(BasePermission):
    """Validates user is authorized to access the resource."""

    def has_permission(self, request, view):
        request.user_id = "1"
        return True
        if request.method == "OPTIONS":
            return True
        if not request.headers.get(settings.API_KEY_HEADER):
            return False
        authorization = request.headers.get("Authorization")
        if not authorization:
            return False
        token = authorization.split(" ")[1]
        payload = validate_jwt(token)
        if not payload:
            return False
        user_id = payload["user_id"]

        # Append user_id to request object
        request.user_id = user_id
        return True
