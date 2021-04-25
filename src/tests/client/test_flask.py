import pytest
import flask
import flask.testing
from client.flask.router import init_router
from usecases.login import LoginTokens
from usecases import exceptions

class MockService:
  def login(self, username: str, password: str) -> LoginTokens:
    return LoginTokens(
      access_token=(username + password + "foo"),
      refresh_token=(username + password + "bar")
    )

class BadService:
  exception: Exception
  def __init__(self, exception: Exception) -> None:
    self.exception = exception
  def login(self, username: str, password: str) -> LoginTokens:
    raise self.exception

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
  assert rv.status_code == 400

def test_login_needs_password(client: flask.testing.FlaskClient):
  rv: flask.Response = client.post('/login', json={
    'username': 'johndoe',
  })
  assert b'Password is required' in rv.data
  assert rv.status_code == 400

def test_login_responds_with_exception(client: flask.testing.FlaskClient):
  badApp = init_router(BadService(Exception('Foo')))
  with badApp.test_client() as c:
    rv: flask.Response = c.post('/login', json={
      'username': 'johndoe',
      'password': 'supersecret'
    })
    assert b'Foo' in rv.data
    assert rv.status_code == 400

  badApp = init_router(BadService(exceptions.Internal()))
  with badApp.test_client() as c:
    rv: flask.Response = c.post('/login', json={
      'username': 'johndoe',
      'password': 'supersecret'
    })
    assert b'Internal error' in rv.data
    assert rv.status_code == 500

def test_login_success(client: flask.testing.FlaskClient):
  rv: flask.Response = client.post('/login', json={
    'username': 'johndoe',
    'password': 'supersecret'
  })
  json_data = rv.get_json()

  assert json_data['access_token'] == "johndoesupersecretfoo"
  assert json_data['refresh_token'] == "johndoesupersecretbar"
