from .service import Service
from client.flask.router import Router

app = Router(Service()).app