from typing import Protocol

class Hasher(Protocol):
  def hash(self, plain_text: str) -> str:
    raise Exception("Not implemented")