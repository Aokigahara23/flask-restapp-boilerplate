from typing import List
from flask import Blueprint

from .kitties import kitties
from .auth import auth

endpoints: List[Blueprint] = [
    kitties,
    auth
]
