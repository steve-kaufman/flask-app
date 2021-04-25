from typing import Protocol

class PasswordMatcher(Protocol):
  def match(self, plain_pass: str, secure_pass: str) -> bool:
    raise Exception("Not implemented")
