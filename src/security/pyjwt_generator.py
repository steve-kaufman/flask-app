import jwt
import time

algorithm = "HS256"

class PyJWTGenerator:
  access_token_secret: str
  refresh_token_secret: str
  def __init__(self, access_secret: str, refresh_secret: str) -> None:
    self.access_token_secret = access_secret
    self.refresh_token_secret = refresh_secret

  def generate_access_token(self, user_id: int, username: str) -> str:
    payload = {
      "user_id": user_id,
      "username": username,
      "iat": time.time()
    }
    # jwt.encode actually returns a string, despite the type hint that says bytes
    access_token = jwt.encode(payload, self.access_token_secret, algorithm)
    return access_token

  def generate_refresh_token(self, user_id: int, username: str) -> str:
    payload = {
      "user_id": user_id,
      "username": username,
      "iat": time.time()
    }
    refresh_token = jwt.encode(payload, self.refresh_token_secret, algorithm)
    return refresh_token