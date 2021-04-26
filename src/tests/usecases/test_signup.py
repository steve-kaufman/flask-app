import pytest
from entities.user import User
from usecases import exceptions
from usecases.signup import SignupDependencies, signup
from tests.usecases.mocks import BadHasher, BadUserCreator, BadUserGetter, MockHasher, MockUserCreator, MockUserGetter

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

def test_raises_internal_err_with_bad_user_getter():
  deps = SignupDependencies(
    user_getter=BadUserGetter(Exception("foo")),
    hasher=MockHasher(),
    user_creator=MockUserCreator()
  )

  with pytest.raises(exceptions.Internal):
    signup(deps, "foo", "bar")

def test_raises_unique_username_err_with_existing_username():
  deps = SignupDependencies(
    user_getter=MockUserGetter(example_users),
    hasher=MockHasher(),
    user_creator=MockUserCreator()
  )

  with pytest.raises(exceptions.NeedUniqueUsername, match='phillipfry'):
    signup(deps, "phillipfry", "supersecret")

def test_raises_internal_err_with_bad_hasher():
  deps = SignupDependencies(
    user_getter=MockUserGetter(example_users),
    hasher=BadHasher(),
    user_creator=MockUserCreator()
  )

  with pytest.raises(exceptions.Internal):
    signup(deps, "newuser", "supersecret")

def test_raises_internal_err_with_bad_user_creator():
  deps = SignupDependencies(
    user_getter=MockUserGetter(example_users),
    hasher=MockHasher(),
    user_creator=BadUserCreator()
  )

  with pytest.raises(exceptions.Internal):
    signup(deps, "newuser", "supersecret")

def test_hashes_password_and_creates_user():
  user_creator=MockUserCreator()
  deps = SignupDependencies(
    user_getter=MockUserGetter(example_users),
    hasher=MockHasher(),
    user_creator=user_creator
  )

  signup(deps, "newuser", "supersecret")

  assert user_creator.created_user == User(
    id=42,
    username="newuser",
    password=MockHasher().hash("supersecret")
  )