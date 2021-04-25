import os
from entities.user import User
from security.fake_hasher import FakeHasher
from security.fake_jwt_generator import FakeJWTGenerator
from security.bcrypt_hasher import BCryptHasher
from security.pyjwt_generator import PyJWTGenerator
from . import router
from usecases.login import LoginDependencies, LoginTokens, login
from db.memory import MemoryDB

jwtGenerator = PyJWTGenerator("foo", "bar")
hasher = BCryptHasher()

example_users: list[User] = [
  User(
    id=1,
    username="phillipfry",
    password=hasher.hash("1234")
  ),
  User(
    id=2,
    username="turangaleela",
    password=hasher.hash("1234")
  ),
  User(
    id=3,
    username="johnzoidberg",
    password=hasher.hash("1234")
  ),
]

db = MemoryDB(example_users)

class FlaskService:
  def login(self, username: str, password: str) -> LoginTokens:
    protocols = LoginDependencies(db, hasher, jwtGenerator)
    return login(protocols, username, password)

app = router.init_router(FlaskService())