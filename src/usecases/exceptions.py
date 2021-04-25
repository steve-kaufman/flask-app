class Internal(Exception):
  message = "Internal error"

class UserNotFound(Exception):
  def __init__(self, username: str):
    super().__init__("No user with username " + username)

class BadPassword(Exception):
  message = "Bad password"