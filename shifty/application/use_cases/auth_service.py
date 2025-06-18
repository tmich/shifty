from passlib.context import CryptContext
from datetime import datetime, timedelta
import datetime as dt
from datetime import timezone
import jwt
import os
from shifty.infrastructure.repositories.auth_sqlalchemy import AuthRepository
from shifty.domain.entities import Auth

class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.jwt_secret = os.getenv("JWT_SECRET_KEY", "dev_secret")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.jwt_exp_minutes = int(os.getenv("JWT_EXP_MINUTES", "60"))

    def signup(self, username: str, password: str) -> Auth:
        password_hash = self.pwd_context.hash(password)
        auth = Auth(username=username, password_hash=password_hash)
        return self.repository.add(auth)

    def authenticate(self, username: str, password: str) -> Auth:
        auth = self.repository.get_by_username(username)

        if not auth or not auth.is_valid:
            raise ValueError("Invalid username or account is not valid")
        
        if not self.pwd_context.verify(password, auth.password_hash):
            raise ValueError("Invalid username or account is not valid")
        
        return auth

    def create_jwt(self, username: str) -> str:
        now = dt.datetime.now(timezone.utc)
        payload = {
            "sub": username,
            "exp": now + timedelta(minutes=self.jwt_exp_minutes),
            "iat": now,
            "aud": "authenticated"
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

    def verify_jwt(self, token: str) -> str:
        payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm], audience="authenticated")
        return payload["sub"]

