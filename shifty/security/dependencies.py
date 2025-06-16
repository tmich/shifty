import os
from fastapi import HTTPException, Request, status
import jwt


def get_current_user_id(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")

    secret_key: str | None = os.getenv("JWT_SECRET_KEY")

    if not secret_key:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="JWT secret key not configured")
    
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    
    token = auth_header[len("Bearer "):]

    try:
        payload = jwt.decode(token, secret_key, algorithms=[JWT_ALGORITHM], audience="authenticated")
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token verification failed")