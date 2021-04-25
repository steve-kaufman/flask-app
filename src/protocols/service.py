from typing import Protocol
from usecases.login import LoginTokens

class Service(Protocol):
  def login(self, username: str, password: str) -> LoginTokens:
    raise Exception("Not implemented")