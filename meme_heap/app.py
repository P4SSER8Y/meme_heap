from typing import List, Optional
import fastapi
import fastapi.staticfiles
from uuid import uuid4
from datetime import datetime
import re
import os
import yaml
import pathlib
import aiofiles
import logging

logger = logging.getLogger("meme")
app = fastapi.APIRouter(tags=['meme'])
statics = {}

DATA_PATH = pathlib.Path(os.environ.get("MEME_DATA_PATH", "./data"))
RAW_DATA_PATH = DATA_PATH.joinpath('raw')
os.makedirs(RAW_DATA_PATH, exist_ok=True)
META_DATA_PATH = DATA_PATH.joinpath('meta')
os.makedirs(META_DATA_PATH, exist_ok=True)
THUMBNAIL_DATA_PATH = DATA_PATH.joinpath('thumbnail')
os.makedirs(THUMBNAIL_DATA_PATH, exist_ok=True)

statics['/raw'] = RAW_DATA_PATH
statics['/thumbnail'] = THUMBNAIL_DATA_PATH

TOKENS = {
    "81fe8bfe87576c3ecb22426f8e57847382917acf": "troy",  # abcd
}


async def get_user_from_token(token: str = fastapi.Header(...)):
    from hashlib import sha1
    token = sha1(token.encode()).hexdigest()
    if token in TOKENS.keys():
        return TOKENS[token]
    else:
        raise fastapi.HTTPException(fastapi.status.HTTP_404_NOT_FOUND)


def get_tags(tag: Optional[str]):
    return [x for x in re.split(r'[,，]', tag) if len(x) > 0]


@app.get('/get_user')
async def get_user(user=fastapi.Depends(get_user_from_token)):
    return {"user": user}


@app.post('/')
async def upload(file: fastapi.UploadFile = fastapi.File(...), tags: str = fastapi.Body(''), user=fastapi.Depends(get_user_from_token)):
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
    return data


@app.get('/')
async def query(tag: List[str] = fastapi.Query(...), user=fastapi.Depends(get_user_from_token)):
    return tag


@app.delete('/')
async def delete(uuid: str = fastapi.Query(...), user=fastapi.Depends(get_user_from_token)):
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
        raise fastapi.HTTPException(fastapi.status.HTTP_404_NOT_FOUND)
    return {"uuid": uuid}


@app.put('/tag/')
async def tag_add(uuid: str = fastapi.Query(...), user=fastapi.Depends(get_user_from_token)):
    pass


@app.delete('/tag/')
async def tag_delete(uuid: str = fastapi.Query(...), user=fastapi.Depends(get_user_from_token)):
    pass
