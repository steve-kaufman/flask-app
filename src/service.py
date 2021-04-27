from usecases.login import LoginDependencies, LoginTokens, login
from usecases.signup import SignupDependencies, signup

from db.sqlite import SQLiteDB
from security.bcrypt_hasher import BCryptHasher
from security.pyjwt_generator import PyJWTGenerator

db = SQLiteDB('flask.db')
hasher = BCryptHasher()
jwtGenerator = PyJWTGenerator("foo", "bar") # replace with real secrets

class Service:
  def login(self, username: str, password: str) -> LoginTokens:
    deps = LoginDependencies(db, hasher, jwtGenerator)
    return login(deps, username, password)
  def signup(self, username: str, password: str) -> None:
    deps = SignupDependencies(db, hasher, db)
    signup(deps, username, password)
