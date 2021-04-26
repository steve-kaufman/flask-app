from db.sqlite import SQLiteDB
from entities.user import User
from usecases.login import LoginDependencies, LoginTokens, login
from security.fake_hasher import FakeHasher
from security.fake_jwt_generator import FakeJWTGenerator
from security.bcrypt_hasher import BCryptHasher
from security.pyjwt_generator import PyJWTGenerator
from client.flask import router

jwtGenerator = PyJWTGenerator("foo", "bar")
hasher = BCryptHasher()

example_users: list[User] = [
  User(
    username="phillipfry",
    password=hasher.hash("pass1")
  ),
  User(
    username="turangaleela",
    password=hasher.hash("pass2")
  ),
  User(
    username="johnzoidberg",
    password=hasher.hash("pass3")
  ),
]

db = SQLiteDB('flask.db')

for user in example_users:
  db.create_user(user)

class FlaskService:
  def login(self, username: str, password: str) -> LoginTokens:
    deps = LoginDependencies(db, hasher, jwtGenerator)
    return login(deps, username, password)

app = router.init_router(FlaskService())