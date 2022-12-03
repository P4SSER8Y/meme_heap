from typing import Optional
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
import os
import pathlib
from . import models
import bcrypt

DATABASE_PATH = pathlib.Path(os.environ.get('MEME_DATA_PATH', './data'), 'sqlite.db')
os.makedirs(DATABASE_PATH.parent, exist_ok=True)
DEFAULT_DB_PATH = "sqlite:///{}".format(DATABASE_PATH)
DB_URL = os.environ.get('MEME_DB_URL', DEFAULT_DB_PATH)

DEFAULT_ADMIN_USER = os.environ.get('MEME_DB_ADMIN', 'admin')
DEFAULT_ADMIN_PASSWORD = os.environ.get('MEME_DB_ADMIN_PASSWORD', 'admin')
DEFAULT_ADMIN_TOKEN = os.environ.get('MEME_DB_ADMIN_TOKEN', 'admin')
TOKEN_SALT = os.environ.get('MEME_TOKEN_SALT', 'memeMEME1v131v13')


engine = create_engine(DB_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()


def get_password_hash(raw: str):
    import bcrypt
    return bcrypt.hashpw(raw.encode('utf-8'), bcrypt.gensalt())


def get_token_hash(raw: str):
    from hashlib import sha1
    return sha1((raw + TOKEN_SALT).encode()).hexdigest()


def create_user(db: Session, name: str, pwd: str, admin: bool = False):
    user = models.User(name=name, admin=admin, password=get_password_hash(pwd))
    db.add(user)
    return {"name": name, "admin": admin}


def delete_user(db: Session, name: str):
    if name == DEFAULT_ADMIN_USER:
        raise Exception('cannot delete default administrator account')
    db.query(models.Tag).filter(models.Tag.owner == name).delete()
    db.query(models.File).filter(models.File.owner == name).delete()
    db.query(models.Token).filter(models.Token.name == name).delete()
    db.query(models.User).filter(models.User.name == name).delete()
    return {'name': name}


def check_user_password(db: Session, name: str, password: str):
    query = db.query(models.User.password).filter(models.User.name == name).one_or_none()
    if query is None:
        return False
    hash = query[0]
    return bcrypt.checkpw(password.encode('utf-8'), hash)


def token_add(db: Session, name: str, token: Optional[str] = None):
    from random import choice
    if token is None:
        token = ""
        for _ in range(32):
            token += choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    sha = get_token_hash(token)
    query = models.Token(name=name, token=sha)
    db.add(query)
    return {"name": name, "token": token}


def token_delete(db: Session, token: str):
    from hashlib import sha1
    db.query(models.Token).filter(models.Token.token == get_token_hash(token)).delete()


def token_get_all(db: Session, name: str):
    return db.query(models.Token).filter(models.Token.name == name).count()


def get_user_from_token(db: Session, token: str):
    return db.query(models.Token).filter(models.Token.token == get_token_hash(token)).first()


def is_user(db: Session, name: str):
    result = db.query(models.User).filter(models.User.name == name).first()
    return (result is not None)


def is_admin(db: Session, name: str):
    result = db.query(models.User).filter(models.User.name == name).first()
    return result and result.admin


def tag_get_all(db: Session, name: str):
    result = db.query(models.Tag.tag, func.count('*').label('count')
                      ).filter(models.Tag.owner == name).group_by(models.Tag.tag).all()
    return result


def tag_add(db: Session, uuid: str, tag: str, owner: str):
    data = models.Tag(uuid=uuid, tag=tag, owner=owner)
    db.add(data)


def tag_delete(db: Session, uuid: str, tag: str, owner: str):
    db.query(models.Tag).filter(models.Tag.uuid == uuid, models.Tag.tag == tag, models.Tag.owner == owner).delete()


def file_add(db: Session, uuid: str, filename: str, owner: str, thumbnail: str):
    data = models.File(uuid=uuid, filename=filename, owner=owner, thumbnail=thumbnail)
    db.add(data)


def file_delete(db: Session, uuid: str):
    db.query(models.Tag).filter(models.Tag.uuid == uuid).delete()
    db.query(models.File).filter(models.File.uuid == uuid).delete()


def get_files_by_tag(db: Session, tag: str, owner: str):
    return db.query(models.Tag.uuid).filter(models.Tag.owner == owner, models.Tag.tag.like(f'%{tag}%')).all()


def get_file_info_by_uuid(db: Session, uuid: str):
    tags = db.query(models.Tag.tag).filter(models.Tag.uuid == uuid).all()
    tags = [x['tag'] for x in tags]
    filename = db.query(models.File).filter(models.File.uuid == uuid).one()
    return {'tags': tags, 'filename': filename.filename, "thumbnail": filename.thumbnail}


def get_all_files(db: Session, owner: str):
    return db.query(models.File.uuid).filter(models.File.owner == owner).all()


def check_if_file_uuid_exist(db: Session, uuid: str, owner: str):
    return db.query(models.File.uuid).filter(models.File.uuid == uuid, models.File.owner == owner).one_or_none() is not None


async def startup():
    try:
        session = SessionLocal()
        if (session.query(models.User).filter(models.User.admin != False).count()) <= 0:
            create_user(session, DEFAULT_ADMIN_USER, DEFAULT_ADMIN_PASSWORD, True)
            token_add(session, DEFAULT_ADMIN_USER, DEFAULT_ADMIN_TOKEN)
            session.commit()
    finally:
        session.close()


async def shutdown():
    session = SessionLocal()
    session.flush()
    session.close_all()
