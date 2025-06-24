from passlib.context import CryptContext
from datetime import datetime, timedelta
import datetime as dt
from datetime import timezone
import jwt
import os
import secrets
from typing import Optional
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
        refresh_token, expiry = self._generate_refresh_token()
        auth = Auth(
            username=username,
            password_hash=password_hash,
            refresh_token=refresh_token,
            refresh_token_expiry=expiry
        )
        return self.repository.add(auth)

    def authenticate(self, username: str, password: str) -> Auth:
        auth = self.repository.get_by_username(username)

        if not auth or not auth.is_valid:
            raise ValueError("Invalid username or account is not valid")

        if not self.pwd_context.verify(password, auth.password_hash):
            raise ValueError("Invalid username or account is not valid")

        # On successful authentication, rotate refresh token
        refresh_token, expiry = self._generate_refresh_token()
        auth.refresh_token = refresh_token
        auth.refresh_token_expiry = expiry
        self.repository.update(auth)
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

    def _generate_refresh_token(self) -> tuple[str, datetime]:
        token = secrets.token_urlsafe(32)
        expiry = dt.datetime.now(timezone.utc) + timedelta(days=7)
        return token, expiry

    def verify_refresh_token(self, username: str, refresh_token: str) -> Optional[Auth]:
        auth = self.repository.get_by_username(username)
        now = dt.datetime.now(timezone.utc)
        if (
            auth and
            auth.refresh_token == refresh_token and
            auth.refresh_token_expiry and
            auth.refresh_token_expiry > now
        ):
            return auth
        return None

    def rotate_refresh_token(self, auth: Auth) -> tuple[str, datetime]:
        refresh_token, expiry = self._generate_refresh_token()
        auth.refresh_token = refresh_token
        auth.refresh_token_expiry = expiry
        self.repository.update(auth)
        return refresh_token, expiry
