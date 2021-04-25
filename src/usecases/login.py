from dataclasses import dataclass
from protocols.db import UserGetter
from protocols.jwt import JWTGenerator
from protocols.password_matcher import PasswordMatcher
from . import exceptions

@dataclass
class LoginDependencies:
  db: UserGetter
  passwd_matcher: PasswordMatcher
  jwt: JWTGenerator

@dataclass
class LoginTokens:
  access_token: str
  refresh_token: str

def login(
  protocols: LoginDependencies,
  username: str, 
  password: str
) -> LoginTokens:
  (db, passwd_matcher, jwt) = (protocols.db, protocols.passwd_matcher, protocols.jwt)

  try:
    user = db.get_user_by_username(username)
  except(exceptions.UserNotFound):
    raise exceptions.UserNotFound(username)
  except Exception as e:
    print(e)
    raise exceptions.Internal()

  try:
    passwd_matches = passwd_matcher.match(password, user.password)
  except:
    raise exceptions.Internal()
  if not passwd_matches:
    raise exceptions.BadPassword()

  try:
    access_token=jwt.generate_access_token(user.id, user.username)
    refresh_token=jwt.generate_refresh_token(user.id, user.username)
  except Exception as e:
    print(e)
    raise exceptions.Internal()

  return LoginTokens(access_token, refresh_token)