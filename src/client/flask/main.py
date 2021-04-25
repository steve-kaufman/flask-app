from . import router
from usecases.login import LoginProtocols, LoginTokens
from db.memory import MemoryDB

class FlaskService:
  def login(self, username: str, password: str) -> LoginTokens:
    return LoginTokens("", "")

app = router.init_router(FlaskService())