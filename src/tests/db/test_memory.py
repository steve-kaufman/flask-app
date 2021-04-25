import pytest
from db.memory import MemoryDB
from entities.user import User
from usecases import exceptions

example_users: list[User] = [
  User(1, "phillipfry", "pass1"),
  User(2, "turangaleela", "pass2"),
  User(3, "johnzoidberg", "pass3"),
]

class TestGetUserByUsername:
  def test_raises_not_found_with_bad_username(self):
    bad_usernames = ["foo", "bar", "baduser", "nobody"]
    for bad_username in bad_usernames:
      memoryDB = MemoryDB(example_users)
      with pytest.raises(exceptions.UserNotFound, match=bad_username):
        memoryDB.get_user_by_username(bad_username)
  def test_returns_correct_user(self):
    for user in example_users:
      memoryDB = MemoryDB(example_users)
      returned_user = memoryDB.get_user_by_username(user.username)
      assert returned_user == user
