from flask import Flask, request, jsonify

from protocols.service import Service
from usecases import exceptions

def login(service: Service):
  data = request.get_json()
  try: 
    username = data['username']
  except:
    return 'Username is required', 400
  try:
    password = data['password']
  except:
    return 'Password is required', 400
  
  try:
    tokens = service.login(username, password)
  except exceptions.Internal as e:
    return str(e), 500
  except Exception as e:
    return str(e), 400

  return jsonify({
    "access_token": tokens.access_token,
    "refresh_token": tokens.refresh_token
  })

def signup(service: Service):
  data = request.get_json()
  try: 
    username = data['username']
  except:
    return 'Username is required', 400
  try:
    password = data['password']
  except:
    return 'Password is required', 400

  try:
    service.signup(username, password)
  except exceptions.Internal as e:
    return str(e), 500
  except Exception as e:
    return str(e), 400

  return 'User successfully created', 201

class Router:
  service: Service
  app: Flask

  def __init__(self, service: Service) -> None:
    self.service = service
    self.app = Flask(__name__)

    self.app.add_url_rule('/login', 'login', self.login, methods=['POST'])
    self.app.add_url_rule('/signup', 'signup', self.signup, methods=['POST'])

  def login(self):
    return login(self.service)
  def signup(self):
    return signup(self.service)