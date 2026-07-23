from .Password import verify_password
from .jwt_handler import create_access_token
from .user_service import create_user

def login(username: str, password: str):

    # Dummy user sementara
    user = {
        "username": "admin",
        "password": "$2b$12$dummyhash"
    }

    token = create_access_token(
        {"sub": username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


def register(user):
    return create_user(user)
