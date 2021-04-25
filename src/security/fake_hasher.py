class FakeHasher:
  def hash(self, plain_text: str) -> str:
    return plain_text + "foo"
  def match(self, plain_pass: str, secure_pass: str) -> bool:
    if self.hash(plain_pass) == secure_pass:
      return True
    return False