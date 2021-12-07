from typing import List
from flask import Blueprint

from .kitties import kitties_endpoint
from .auth import auth_endpoint

endpoints: List[Blueprint] = [
    kitties_endpoint,
    auth_endpoint
]
