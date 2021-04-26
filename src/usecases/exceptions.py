from _pytest._code.code import ExceptionChainRepr


class Internal(Exception):
  def __init__(self):
    super().__init__("Internal error")

class UserNotFound(Exception):
  def __init__(self, username: str):
    super().__init__("No user with username " + username)

class BadPassword(Exception):
  def __init__(self) -> None:
      super().__init__("Bad password")

class NeedUniqueUsername(Exception):
  def __init__(self, username: str) -> None:
      super().__init__("User with username " + username + " already exists")