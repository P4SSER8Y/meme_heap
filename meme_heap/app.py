from typing import List, Optional
import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi import Depends, HTTPException, status, Query, Body
from uuid import uuid4
from datetime import datetime
import re
import os
import yaml
import pathlib
import aiofiles
import logging
from . import crud

logger = logging.getLogger("meme")
app = fastapi.APIRouter()
statics = {}

DATA_PATH = pathlib.Path(os.environ.get("MEME_DATA_PATH", "./data"))
RAW_DATA_PATH = DATA_PATH.joinpath('raw')
os.makedirs(RAW_DATA_PATH, exist_ok=True)
META_DATA_PATH = DATA_PATH.joinpath('meta')
os.makedirs(META_DATA_PATH, exist_ok=True)
THUMBNAIL_DATA_PATH = DATA_PATH.joinpath('thumbnail')
os.makedirs(THUMBNAIL_DATA_PATH, exist_ok=True)


def statics_handler(app: fastapi.FastAPI, prefix: str):
    app.mount(f"{prefix}/raw", StaticFiles(directory=RAW_DATA_PATH))
    app.mount(f"{prefix}/thumbnail", StaticFiles(directory=THUMBNAIL_DATA_PATH))
    app.mount(f"{prefix}/ui", StaticFiles(directory=pathlib.Path(__file__).parent.joinpath('meme_ui/dist'), html=True, check_dir=False))


async def get_user_from_token(token: str = Query(...), db=Depends(crud.get_db)):
    user = crud.get_user_from_token(db, token)
    if user:
        return user.name
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


def get_tags(tag: Optional[str]):
    if tag is None:
        return []
    return [x.strip() for x in re.split(r'[,，]', tag) if len(x) > 0]


@app.post('/', tags=['meme'])
async def upload(file: fastapi.UploadFile = fastapi.File(...), tags: str = fastapi.Body(''), user=Depends(get_user_from_token), db=Depends(crud.get_db)):
    uuid = str(uuid4())
    tags = get_tags(tags)
    ext = pathlib.Path(file.filename).suffix
    size = 0
    ts = datetime.now()
    filename = f"{uuid}{ext}"
    os.makedirs(pathlib.Path(DATA_PATH), exist_ok=True)
    async with aiofiles.open(pathlib.Path(RAW_DATA_PATH, filename), 'wb') as f:
        while True:
            raw = await file.read(32 * 1024 * 1024)
            if len(raw) == 0:
                break
            size += len(raw)
            await f.write(raw)
    data = {"uuid": uuid, "tags": tags, "size": size, "timestamp": ts,
            "content-type": file.content_type, "filename": filename, "owner": user}
    with open(pathlib.Path(META_DATA_PATH, f"{uuid}.yml"), 'w') as f:
        yaml.dump(data, f)
    crud.file_add(db, uuid, filename, user)
    for tag in tags:
        crud.tag_add(db, uuid, tag, user)
    return data


@app.get('/', tags=['meme'])
async def query(tag: str = Query(None), user=Depends(get_user_from_token), db=Depends(crud.get_db)):
    tags = get_tags(tag)
    result = crud.get_all_files(db, user)
    for i in range(0, len(tags)):
        t = crud.get_files_by_tag(db, tags[i], user)
        result = [x for x in result if x in t]
    print(result)
    result = [crud.get_file_info_by_uuid(db, x[0]) for x in result]
    return result


@app.delete('/', tags=['meme'])
async def delete(uuid: str = Query(...), user=Depends(get_user_from_token), db=Depends(crud.get_db)):
    try:
        meta_path = META_DATA_PATH.joinpath(f'{uuid}.yml')
        with open(meta_path, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        if data.get('owner', None) != user:
            raise Exception('owner not match')
        os.remove(meta_path)

        filename = data.get('filename', None)
        if filename is None:
            raise Exception("path is empty")
        file_path = RAW_DATA_PATH.joinpath(filename)
        os.remove(file_path)

        thumbnail = data.get('thumbnail', None)
        if thumbnail:
            thumbnail_path = THUMBNAIL_DATA_PATH.joinpath(thumbnail)
            os.remove(thumbnail_path)

    except Exception as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return {"uuid": uuid}


@app.get('/tag/', tags=['tags'])
async def get_all_tags(user=Depends(get_user_from_token), db=Depends(crud.get_db)):
    return crud.tag_get_all(db, user)


@app.put('/tag/', tags=['tags'])
async def add_tag(tag: str = Query(...), uuid: str = Query(...), user=Depends(get_user_from_token), db=Depends(crud.get_db)):
    if not crud.check_if_file_uuid_exist(db, uuid, user):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    tags = get_tags(tag)
    for item in tags:
        crud.tag_add(db, uuid, item, user)
    return {'uuid': uuid, 'tags': tags}


@app.delete('/tag/', tags=['tags'])
async def delete_tag(tag: str = Query(...), uuid: str = Query(...), user=Depends(get_user_from_token), db=Depends(crud.get_db)):
    if not crud.check_if_file_uuid_exist(db, uuid, user):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    tags = get_tags(tag)
    for item in tags:
        crud.tag_delete(db, uuid, item, user)
    return {'uuid': uuid, 'tags': tags}


# @app.get('/user/', tags=['user'])
# async def get_user(user=Depends(get_user_from_token), db=Depends(crud.get_db)):
#     return {"user": user, 'admin': crud.is_admin(db, user)}


@app.put('/user/', tags=['user'])
async def new_user(name: str = Body(...), password: str = Body(...), user=Depends(get_user_from_token), db=Depends(crud.get_db)):
    if not crud.is_admin(db, user):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    if crud.is_user(db, name):
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    return crud.create_user(db, name, password)


@app.delete('/user/', tags=['user'])
async def delete_user(name: str = Body(...), password: str = Body(...), db=Depends(crud.get_db)):
    if not crud.check_user_password(db, name, password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return crud.delete_user(db, name)


@app.put('/user/token/', tags=['user'])
async def add_token(name: str = Body(...), password: str = Body(...), db=Depends(crud.get_db)):
    if not crud.check_user_password(db, name, password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return crud.token_add(db, name)


@app.delete('/user/token/', tags=['user'])
async def delete_token(name: str = Body(...), password: str = Body(...), token: str = Body(...), db=Depends(crud.get_db)):
    if not crud.check_user_password(db, name, password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    crud.token_delete(db, token)
    return {'name': name, 'token': token}
