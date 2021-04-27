from usecases.login import LoginTokens

class MockService:
  username_signed_up: str
  password_signed_up: str

  def login(self, username: str, password: str) -> LoginTokens:
    return LoginTokens(
      access_token=(username + password + "foo"),
      refresh_token=(username + password + "bar")
    )
  def signup(self, username: str, password: str) -> None:
    self.username_signed_up = username
    self.password_signed_up = password

class BadService:
  exception: Exception
  def __init__(self, exception: Exception) -> None:
    self.exception = exception
  def login(self, username: str, password: str) -> LoginTokens:
    raise self.exception
  def signup(self, username: str, password: str) -> None:
    raise self.exception