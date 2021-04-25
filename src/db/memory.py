from entities.user import User
from usecases.exceptions import UserNotFound

class MemoryDB:
  users: list[User]

  def __init__(self, users: list[User]) -> None:
    self.users = users.copy()
    print(self.users)
  def get_user_by_username(self, username: str) -> User:
    for user in self.users:
      if user.username == username:
        return user
    raise UserNotFound(username)