class Internal(Exception):
  def __init__(self):
    super().__init__("Internal error")

class UserNotFound(Exception):
  def __init__(self, username: str):
    super().__init__("No user with username " + username)

class BadPassword(Exception):
  def __init__(self) -> None:
      super().__init__("Bad password")