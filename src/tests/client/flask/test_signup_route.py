import flask
import flask.testing
import pytest
from usecases import exceptions
from client.flask.router import Router
from tests.client.flask.mocks import MockService, BadService

service = MockService()
app = Router(service).app

@pytest.fixture
def client():
  app.config['TESTING'] = True
  with app.test_client() as client:
    return client
    
def test_needs_method_post(client: flask.testing.FlaskClient):
  rv: flask.Response = client.get('/signup')
  assert rv.status_code == 405
  rv: flask.Response = client.patch('/signup')
  assert rv.status_code == 405
  rv: flask.Response = client.put('/signup')
  assert rv.status_code == 405
  rv: flask.Response = client.delete('/signup')
  assert rv.status_code == 405

def test_needs_username(client: flask.testing.FlaskClient):
  rv: flask.Response = client.post('/signup', json={})
  assert b'Username is required' in rv.data
  rv: flask.Response = client.post('/signup', json={ 
    'password': '1234'
  })
  assert b'Username is required' in rv.data
  assert rv.status_code == 400

def test_needs_password(client: flask.testing.FlaskClient):
  rv: flask.Response = client.post('/signup', json={
    'username': 'johndoe',
  })
  assert b'Password is required' in rv.data
  assert rv.status_code == 400

def test_responds_with_exception_message(client: flask.testing.FlaskClient):
  badApp = Router(BadService(Exception('Foo'))).app
  with badApp.test_client() as c:
    rv: flask.Response = c.post('/signup', json={
      'username': 'johndoe',
      'password': 'supersecret'
    })
    assert b'Foo' in rv.data
    assert rv.status_code == 400

  badApp = Router(BadService(exceptions.Internal())).app
  with badApp.test_client() as c:
    rv: flask.Response = c.post('/signup', json={
      'username': 'johndoe',
      'password': 'supersecret'
    })
    assert b'Internal error' in rv.data
    assert rv.status_code == 500

def test_calls_signup_with_username_and_password(client: flask.testing.FlaskClient):
  client.post('/signup', json={
    'username': 'newuser',
    'password': '1234'
  })
  assert service.username_signed_up == 'newuser'
  assert service.password_signed_up == '1234'

def test_responds_with_success(client: flask.testing.FlaskClient):
  rv: flask.Response = client.post('/signup', json={
    'username': 'johndoe',
    'password': 'supersecret'
  })
  assert b'User successfully created' in rv.data
  assert rv.status_code == 201

