from .Password import hash_password

users = []

def create_user(user):

    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "full_name": user.full_name,
        "role": user.role
    }

    users.append(new_user)

    return {
        "message": "User berhasil disimpan",
        "user": new_user
    }
