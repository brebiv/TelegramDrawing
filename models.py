from sqlalchemy import Column, Integer, String
from database_connect import Base, engine
from telegram import User as tgUser


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tid = Column(Integer, nullable=False, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    lang_code = Column(String)
    link = Column(String)

    def __init__(self, user: tgUser):
        """Create database User entity from Telegram user object"""
        self.tid = user.id
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.username = user.username
        self.link = user.link

    def __repr__(self):
        return f"{self.id} {self.username}"


if __name__ == '__main__':
    Base.metadata.create_all(engine)
