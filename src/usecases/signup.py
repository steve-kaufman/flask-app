from entities.user import User
from . import exceptions
from dataclasses import dataclass
from protocols.db import UserCreator, UserGetter
from protocols.hasher import Hasher

@dataclass
class SignupDependencies:
  user_getter: UserGetter
  hasher: Hasher
  user_creator: UserCreator

def signup(deps: SignupDependencies, username: str, password: str) -> None:
  if not _username_is_unique(deps.user_getter, username):
    raise exceptions.NeedUniqueUsername("phillipfry")

  hashed_pass = _hash_password(deps.hasher, password)
  _create_user(deps.user_creator, username, hashed_pass)

def _username_is_unique(user_getter: UserGetter, username: str) -> bool:
  try:
    user_getter.get_user_by_username(username)
  except exceptions.UserNotFound:
    return True
  except:
    raise exceptions.Internal()
  return False

def _hash_password(hasher: Hasher, password: str) -> str:
  try:
    hashed_pass = hasher.hash(password)
  except Exception as e:
    print(e)
    raise exceptions.Internal()
  return hashed_pass

def _create_user(user_creator: UserCreator, username: str, hashed_pass: str) -> None:
  try:
    user_creator.create_user(User(
      username=username,
      password=hashed_pass
    ))
  except Exception as e:
    print(e)
    raise exceptions.Internal()
