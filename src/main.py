from service import Service
from client.flask.router import Router

app = Router(Service()).app

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')