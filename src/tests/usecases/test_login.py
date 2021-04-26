import pytest
from entities.user import User
from usecases import exceptions
from usecases.login import login, LoginDependencies
from tests.usecases.mocks import MockHasher, MockUserGetter, MockPasswordMatcher, MockJWTGenerator, BadUserGetter, BadPasswordMatcher, BadJWTGenerator

example_users: list[User] = [
  User(
    id=1,
    username="phillipfry",
    password=MockHasher().hash("1234")
  ),
  User(
    id=2,
    username="turangaleela",
    password=MockHasher().hash("1234")
  ),
  User(
    id=3,
    username="johnzoidberg",
    password=MockHasher().hash("1234")
  ),
]

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
    protocols = LoginDependencies(
      db=BadUserGetter(test_case["db_err"]),
      passwd_matcher=MockPasswordMatcher(),
      jwt=MockJWTGenerator()
    )
    with pytest.raises(test_case["expected_err"]):
      login(protocols, "foo", "bar")

def test_throws_not_found_with_bad_username():
  protocols = LoginDependencies(
    db=MockUserGetter(example_users),
    passwd_matcher=MockPasswordMatcher(),
    jwt=MockJWTGenerator()
  )
  with pytest.raises(exceptions.UserNotFound):
    login(protocols, "foo", "bar")

def test_throws_bad_password():
  bad_passwords = ["badpassword", "foo", "bar"]
  for bad_password in bad_passwords:
    protocols = LoginDependencies(
      db=MockUserGetter(example_users),
      passwd_matcher=MockPasswordMatcher(),
      jwt=MockJWTGenerator()
    )
    with pytest.raises(exceptions.BadPassword):
      login(protocols, "phillipfry", bad_password)

def test_throws_internal_when_check_passwd_errors():
  protocols = LoginDependencies(
    db=MockUserGetter(example_users),
    passwd_matcher=BadPasswordMatcher(),
    jwt=MockJWTGenerator()
  )
  with pytest.raises(exceptions.Internal):
    login(protocols, "phillipfry", "1234")

def test_throws_internal_when_jwt_errors():
  protocols = LoginDependencies(
    db=MockUserGetter(example_users),
    passwd_matcher=MockPasswordMatcher(),
    jwt=BadJWTGenerator()
  )
  with pytest.raises(exceptions.Internal):
    login(protocols, "phillipfry", "1234")

def test_returns_access_and_refresh_token():
  protocols = LoginDependencies(
    db=MockUserGetter(example_users),
    passwd_matcher=MockPasswordMatcher(),
    jwt=MockJWTGenerator()
  )
  tokens = login(protocols, "phillipfry", "1234")
  assert tokens.access_token == "phillipfry1foo"
  assert tokens.refresh_token == "1phillipfryfoo"
