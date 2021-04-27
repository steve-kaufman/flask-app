from typing import Tuple
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.engine import Engine
import sqlalchemy.orm
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from entities.user import User
from usecases import exceptions

Base = declarative_base()

class UserModel(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String)
  password = Column(String)

class SQLiteDB:
  Session: sqlalchemy.orm.Session

  def __init__(self, location: str) -> None:
    engine = create_engine('sqlite:///' + location, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    self.Session = Session

  def create_user(self, user: User) -> None:
    user_model = UserModel(username=user.username, password=user.password)
    session = self.Session()
    session.add(user_model)
    session.commit()

  def get_user_by_username(self, username: str) -> User:
    user_model: UserModel = self.Session().query(UserModel).where(
      UserModel.username == username
    ).first()
    if not user_model:
      raise exceptions.UserNotFound(username)
    return User(user_model.id, user_model.username, user_model.password)