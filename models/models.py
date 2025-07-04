from db.db import Base
from sqlalchemy import String, Text , Boolean, Integer, Column, VARCHAR, INTEGER


class Users(Base):
    __tablename__ = "users"
    id = Column(INTEGER,primary_key=True)
    username = Column(VARCHAR(10))
    password = Column(Text)


class Video(Base):
    __tablename__ = "videos"
    id = Column(INTEGER, primary_key=True)
    url = Column(Text)
    user = Column(Text)
    title= Column(Text)

    # def __repr__(self):
    #     return (
    #         f"<Video(id={self.id!r}, user={self.user!r}, url={self.url!r})>"
    #     )


class Subs(Base):
    __tablename__ = "subs"
    id = Column(INTEGER, primary_key=True)
    subscriber = Column(Text)
    subbed = Column(Text)
    

class Likes(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    url =  Column(Text)
    user = Column(Text)


class Comments(Base):
    __tablename__= "comments"
    id = Column(Integer, primary_key=True)
    url =  Column(Text)
    user = Column(Text)
    comment = Column(Text)