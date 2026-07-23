from fastapi import APIRouter

router = APIRouter()

users = [
    {
        "username": "owner",
        "password": "123456",
        "role": "Owner"
    }
]

@router.post("/login")
def login(data: dict):

    for user in users:
        if (
            data["username"] == user["username"]
            and
            data["password"] == user["password"]
        ):
            return {
                "message": "Login berhasil",
                "role": user["role"]
            }

    return {
        "message": "Username atau Password salah"
          }
