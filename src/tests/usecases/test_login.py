import pytest
from usecases.login import login, LoginProtocols
from usecases import exceptions
from entities.user import User

def mockHash(passwd: str) -> str:
  return passwd + "foo"

class MockPasswordMatcher:
  def match(self, plain_pass: str, secure_pass: str) -> bool:
    if mockHash(plain_pass) == secure_pass:
      return True
    return False

class MockJWTGenerator:
  def generate_access_token(self, user_id: int, username: str) -> str:
    return username + str(user_id) + "foo"
  def generate_refresh_token(self, user_id: int, username: str) -> str:
    return str(user_id) + username + "foo"

example_users: list[User] = [
  User(
    id=1,
    username="phillipfry",
    password=mockHash("1234")
  ),
  User(
    id=2,
    username="turangaleela",
    password=mockHash("1234")
  ),
  User(
    id=3,
    username="johnzoidberg",
    password=mockHash("1234")
  ),
]

class ErrorDB:
  exception: Exception
  def __init__(self, exception: Exception):
    self.exception = exception
  def get_user_by_username(self, username: str) -> User:
    raise self.exception

class MockDB:
  def get_user_by_username(self, username: str) -> User:
    for user in example_users:
      if user.username == username:
        return user
    raise exceptions.UserNotFound(username)

db_error_tests = [
  {
    "db_err": Exception("Foo"),
    "expected_err": exceptions.Internal,
  },
  {
    "db_err": Exception("Bar"),
    "expected_err": exceptions.Internal,
  },
  {
    "db_err": ZeroDivisionError,
    "expected_err": exceptions.Internal,
  },
  {
    "db_err": exceptions.UserNotFound(""),
    "expected_err": exceptions.UserNotFound,
  },
]

def test_censors_db_errors():
  for test_case in db_error_tests:
    protocols = LoginProtocols(
      db=ErrorDB(test_case["db_err"]),
      passwd_matcher=MockPasswordMatcher(),
      jwt=MockJWTGenerator()
    )
    with pytest.raises(test_case["expected_err"]):
      login(protocols, "foo", "bar")

def test_throws_not_found_with_bad_username():
  protocols = LoginProtocols(
    db=MockDB(),
    passwd_matcher=MockPasswordMatcher(),
    jwt=MockJWTGenerator()
  )
  with pytest.raises(exceptions.UserNotFound):
    login(protocols, "foo", "bar")

def test_throws_bad_password():
  bad_passwords = ["badpassword", "foo", "bar"]
  for bad_password in bad_passwords:
    protocols = LoginProtocols(
      db=MockDB(),
      passwd_matcher=MockPasswordMatcher(),
      jwt=MockJWTGenerator()
    )
    with pytest.raises(exceptions.BadPassword):
      login(protocols, "phillipfry", bad_password)

def test_returns_access_and_refresh_token():
  protocols = LoginProtocols(
    db=MockDB(),
    passwd_matcher=MockPasswordMatcher(),
    jwt=MockJWTGenerator()
  )
  tokens = login(protocols, "phillipfry", "1234")
  assert tokens.access_token == "phillipfry1foo"
  assert tokens.refresh_token == "1phillipfryfoo"