__all__ = ('endpoints',)

from src.endpoints.auth import auth_endpoint

endpoints = [
    auth_endpoint
]
