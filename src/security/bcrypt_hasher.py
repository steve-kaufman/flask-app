import bcrypt

class BCryptHasher:
  def hash(self, plain_text: str) -> str:
    hash_bytes = bcrypt.hashpw(bytes(plain_text, 'utf-8'), bcrypt.gensalt())
    return hash_bytes.decode('utf-8')
  def match(self, plain_pass: str, secure_pass: str) -> bool:
    plain_pass_bytes = bytes(plain_pass, 'utf-8')
    secure_pass_bytes = bytes(secure_pass, 'utf-8')
    return bcrypt.checkpw(plain_pass_bytes, secure_pass_bytes)