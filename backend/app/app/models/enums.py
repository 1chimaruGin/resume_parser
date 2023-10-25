# pylint: disable=invalid-name
"""Define Enums for this project."""
from enum import Enum


class RoleType(Enum):
    user = "user"
    admin = "admin"
    guest = "guest"
    organization = "organization"