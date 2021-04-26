import os
import pytest
import sqlite3

from db.sqlite import SQLiteDB
from usecases import exceptions
from entities.user import User

db_location = 'test.db'

@pytest.fixture
def con() -> sqlite3.Connection:
  con = sqlite3.connect(db_location)
  yield con

  con.close()
  os.remove(db_location)

def test_create_user_inserts_user(con: sqlite3.Connection):
  sqlite_db = SQLiteDB(db_location)
  sqlite_db.create_user(User(-7, "foo", "bar"))
  cur = con.cursor()
  cur.execute('SELECT id, username, password FROM users WHERE id = 1')
  (id, username, password) = cur.fetchone()
  assert id == 1
  assert username == "foo"
  assert password == "bar"

def test_get_user_by_username_raises_not_found():
  sqlite_db = SQLiteDB(db_location)
  with pytest.raises(exceptions.UserNotFound, match="foo"):
    sqlite_db.get_user_by_username("foo")

def test_get_user_by_username_returns_correct_user(con: sqlite3.Connection):
  sqlite_db = SQLiteDB(db_location)
  cur = con.cursor()
  dummy_users = [
    {"username": "user1", "password": "pass1"},
    {"username": "user2", "password": "pass2"},
    {"username": "user3", "password": "pass3"},
  ]
  cur.executemany(
    'INSERT INTO users (username, password) VALUES (:username, :password)', 
    dummy_users
  )
  con.commit()

  user1 = sqlite_db.get_user_by_username('user1')
  assert user1.id == 1
  assert user1.username == "user1"
  assert user1.password == "pass1"

  user2 = sqlite_db.get_user_by_username('user2')
  assert user2.id == 2
  assert user2.username == "user2"
  assert user2.password == "pass2"
