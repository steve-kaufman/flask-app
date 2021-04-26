from typing import Protocol
from entities.user import User

class UserGetter(Protocol):
  def get_user_by_username(self, username: str) -> User:
    raise Exception("Not implemented")

class UserCreator(Protocol):
  def create_user(self, user: User) -> None:
    raise Exception("Not implemented")