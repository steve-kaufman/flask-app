class WeakHasher:
  def hash(self, plain_text: str) -> str:
    return plain_text + "foo"
  def match(self, plain_text: str, hash: str) -> bool:
    if self.hash(plain_text) == hash:
      return True
    return False