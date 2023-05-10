from enum import Enum


class AuthProvider(str, Enum):
    Google = "google"
    Facebook = "facebook"
