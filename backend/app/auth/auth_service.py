from .Password import verify_password
from .jwt_handler import create_access_token

def login(username: str, password: str):

    # Dummy user sementara
    user = {
        "username": "admin",
        "password": "$2b$12$dummyhash"
    }
def register(user):

    return {
        "message": "User berhasil dibuat",
        "username": user.username,
        "email": user.email
    }
    token = create_access_token(
        {"sub": username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
