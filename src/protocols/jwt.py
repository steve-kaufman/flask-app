from typing import Protocol

class JWTGenerator(Protocol):
  def generate_access_token(self, user_id: int, username: str) -> str:
    raise Exception("Not implemented")
  def generate_refresh_token(self, user_id: int, username: str) -> str:
    raise Exception("Not implemented")