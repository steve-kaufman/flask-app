from dataclasses import dataclass

@dataclass
class User:
  id: int = 0
  username: str = ""
  password: str = ""
