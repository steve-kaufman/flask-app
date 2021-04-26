from usecases import exceptions
from entities.user import User

class BadHasher:
  def hash(self, plain_text: str) -> str:
    raise Exception("foo")

class MockHasher:
  def hash(self, plain_text: str) -> str:
    return plain_text + "foo"

class MockPasswordMatcher:
  def match(self, plain_pass: str, secure_pass: str) -> bool:
    if MockHasher().hash(plain_pass) == secure_pass:
      return True
    return False

class BadPasswordMatcher:
  def match(self, plain_pass: str, secure_pass: str) -> bool:
    raise Exception("Foo")

class MockJWTGenerator:
  def generate_access_token(self, user_id: int, username: str) -> str:
    return username + str(user_id) + "foo"
  def generate_refresh_token(self, user_id: int, username: str) -> str:
    return str(user_id) + username + "foo"

class BadJWTGenerator:
  def generate_access_token(self, user_id: int, username: str) -> str:
    raise Exception("foo")
  def generate_refresh_token(self, user_id: int, username: str) -> str:
    raise Exception("bar")


class BadUserGetter:
  exception: Exception
  def __init__(self, exception: Exception):
    self.exception = exception
  def get_user_by_username(self, username: str) -> User:
    raise self.exception

class MockUserGetter:
  users: list[User]
  def __init__(self, users: list[User]) -> None:
      self.users = users
  def get_user_by_username(self, username: str) -> User:
    for user in self.users:
      if user.username == username:
        return user
    raise exceptions.UserNotFound(username)

class BadUserCreator:
  def create_user(self, user: User) -> None:
    raise Exception("foo")

class MockUserCreator:
  created_user: User
  def create_user(self, user: User) -> None:
    user.id = 42
    self.created_user = user