from flask import Flask, request, jsonify

from protocols.service import Service
from usecases import exceptions

def init_router(service: Service) -> Flask:
  app = Flask(__name__)

  @app.route('/login', methods=['POST'])
  def login():
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

  return app