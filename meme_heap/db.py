from typing import Optional
from sqlalchemy import Column, String, Integer, create_engine, Table, MetaData, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import asyncio
import os
import pathlib
import hashlib

DEFAULT_DB_PATH = "sqlite:///{}".format(pathlib.Path(os.environ.get('MEME_DATA_PATH', './data'), 'sqlite.db'))
DB_URL = os.environ.get('MEME_DB_URL', DEFAULT_DB_PATH)

DEFAULT_ADMIN_USER = os.environ.get('MEME_DB_ADMIN', 'admin')
DEFAULT_ADMIN_TOKEN = os.environ.get('MEME_DB_ADMIN_TOKEN', 'admin')

engine = create_engine(DB_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'

    user = Column(String(length=32), index=True, primary_key=True)
    admin = Column(Boolean, default=True)


class Token(Base):
    __tablename__ = 'Token'
    token = Column(String(length=40), unique=True, index=True, primary_key=True)
    user = Column('user', ForeignKey('User.user'))


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(db: Session, user: str, admin: bool = False):
    user = User(user=user, admin=admin)
    db.add(user)
    db.commit()
    return {"user": user, "admin": admin}


def add_token(db: Session, user: str, token: Optional[str]):
    from random import choice
    if token is None:
        token = ""
        for _ in range(64):
            token += choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    sha = hashlib.sha1(token.encode()).hexdigest()
    query = Token(user=user, token=sha)
    db.add(query)
    db.commit()
    return {"user": user, "token": token}


def get_user(db: Session, token: str):
    return db.query(Token).filter(Token.token == token).first()


async def startup():
    query = "SELECT COUNT(*) FROM user WHERE user.admin=1"
    try:
        session = SessionLocal()
        if (session.query(User).filter(User.admin != False).count()) <= 0:
            create_user(session, DEFAULT_ADMIN_USER, True)
            add_token(session, DEFAULT_ADMIN_USER, DEFAULT_ADMIN_TOKEN)
    finally:
        session.close()


async def shutdown():
    session = SessionLocal()
    session.flush()
    session.close_all()
