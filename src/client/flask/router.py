from flask import Flask, request, jsonify

from protocols.service import Service

def init_router(service: Service) -> Flask:
  app = Flask(__name__)

  @app.route('/login', methods=['POST'])
  def login():
    data = request.get_json()
    try: 
      username = data['username']
    except:
      return 'Username is required'
    try:
      password = data['password']
    except:
      return 'Password is required'
    
    tokens = service.login(username, password)
    return jsonify({
      "access_token": tokens.access_token,
      "refresh_token": tokens.refresh_token
    })

  return app