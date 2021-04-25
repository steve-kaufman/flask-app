class FakeJWTGenerator:
  def generate_access_token(self, user_id: int, username: str) -> str:
    return username + str(user_id) + "foo"
  def generate_refresh_token(self, user_id: int, username: str) -> str:
    return str(user_id) + username + "foo"