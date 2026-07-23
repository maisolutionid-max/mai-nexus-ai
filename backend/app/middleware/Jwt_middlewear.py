from fastapi import HTTPException
from jose import jwt

SECRET_KEY = "mai_nexus_ai_secret"
ALGORITHM = "HS256"

def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Token tidak valid"
        )
