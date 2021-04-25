import pytest
import flask
import flask.testing
from client.flask.router import init_router
from usecases.login import LoginTokens

class MockService:
  def login(self, username: str, password: str) -> LoginTokens:
    return LoginTokens(
      access_token=(username + password + "foo"),
      refresh_token=(username + password + "bar")
    )

app = init_router(MockService())

@pytest.fixture
def client():
  app.config['TESTING'] = True
  with app.test_client() as client:
    return client

def test_login_needs_method_post(client: flask.testing.FlaskClient):
  rv: flask.Response = client.get('/login')
  assert rv.status_code == 405
  rv: flask.Response = client.patch('/login')
  assert rv.status_code == 405
  rv: flask.Response = client.put('/login')
  assert rv.status_code == 405
  rv: flask.Response = client.delete('/login')
  assert rv.status_code == 405

def test_login_needs_username(client: flask.testing.FlaskClient):
  rv: flask.Response = client.post('/login', json={})
  assert b'Username is required' in rv.data
  rv: flask.Response = client.post('/login', json={ 
    'password': '1234'
  })
  assert b'Username is required' in rv.data

def test_login_needs_password(client: flask.testing.FlaskClient):
  rv: flask.Response = client.post('/login', json={
    'username': 'johndoe',
  })
  assert b'Password is required' in rv.data

def test_login_calls_service(client: flask.testing.FlaskClient):
  rv: flask.Response = client.post('/login', json={
    'username': 'johndoe',
    'password': 'supersecret'
  })
  json_data = rv.get_json()

  assert json_data['access_token'] == "johndoesupersecretfoo"
  assert json_data['refresh_token'] == "johndoesupersecretbar"
