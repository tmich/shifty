from sqlmodel import Session, select
from shifty.domain.entities import Auth
from uuid import UUID
from typing import Optional

class AuthRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> Optional[Auth]:
        return self.session.exec(select(Auth).where(Auth.username == username)).first()

    def add(self, auth: Auth) -> Auth:
        self.session.add(auth)
        self.session.commit()
        self.session.refresh(auth)
        return auth

    def set_validity(self, username: str, is_valid: bool):
        auth = self.get_by_username(username)
        if auth:
            auth.is_valid = is_valid
            self.session.add(auth)
            self.session.commit()
            self.session.refresh(auth)
        return auth
