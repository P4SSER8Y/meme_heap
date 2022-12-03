from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Table, MetaData, Boolean, ForeignKey

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    name = Column(String(length=32), index=True, primary_key=True, nullable=False)
    password = Column(String(length=40), nullable=False)
    admin = Column(Boolean, default=True)


class Token(Base):
    __tablename__ = 'Token'
    token = Column(String(length=40), unique=True, index=True, primary_key=True)
    name = Column(ForeignKey('User.name'), nullable=False)


class Tag(Base):
    __tablename__ = 'Tag'
    id = Column(Integer, index=True, primary_key=True, nullable=False, autoincrement=True)
    uuid = Column(String(length=36), ForeignKey('File.uuid'), nullable=False)
    tag = Column(String(length=64), nullable=False)
    owner = Column(ForeignKey('User.name'))


class File(Base):
    __tablename__ = 'File'
    uuid = Column(String(length=36), primary_key=True, nullable=False)
    filename = Column(String(length=128), nullable=False)
    thumbnail = Column(String(length=128), nullable=True)
    owner = Column(ForeignKey('User.name'))
