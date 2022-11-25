from typing import List
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
app = fastapi.FastAPI()

DATA_PATH = os.environ.get("MEME_DATA_PATH", "./static")

TOKENS = {
    "81fe8bfe87576c3ecb22426f8e57847382917acf": "troy",  # abcd
}

for user in TOKENS.values():
    path = pathlib.Path(DATA_PATH).joinpath(user)
    os.makedirs(path, exist_ok=True)


async def get_user_from_token(token: str = fastapi.Header(None)):
    from hashlib import sha1
    token = sha1(token.encode()).hexdigest()
    if token in TOKENS.keys():
        return TOKENS[token]
    else:
        raise fastapi.HTTPException(fastapi.status.HTTP_404_NOT_FOUND)


app.mount("/static", fastapi.staticfiles.StaticFiles(directory=DATA_PATH), "static")


@app.get('/get_user')
async def get_user(user=fastapi.Depends(get_user_from_token)):
    return {"user": user}


@app.post('/')
async def upload(file: fastapi.UploadFile = fastapi.File(...), tags: str = fastapi.Body(...), user=fastapi.Depends(get_user_from_token)):
    uuid = str(uuid4())
    tags = re.split(r"[,，]", tags)
    ext = pathlib.Path(file.filename).suffix
    size = 0
    ts = datetime.now()
    parent = pathlib.Path(user)
    filename = f"{uuid}{ext}"
    os.makedirs(pathlib.Path(DATA_PATH, parent), exist_ok=True)
    async with aiofiles.open(pathlib.Path(DATA_PATH, parent, filename), 'wb') as f:
        while True:
            raw = await file.read(32 * 1024 * 1024)
            if len(raw) == 0:
                break
            size += len(raw)
            await f.write(raw)
    data = {"uuid": uuid, "tags": tags, "size": size, "timestamp": ts,
           "content-type": file.content_type, "path": str(parent.joinpath(filename))}
    with open(pathlib.Path(DATA_PATH, parent, f"{uuid}_meta.yml"), 'w') as f:
        yaml.dump(data, f)
    return data


@app.get('/')
async def query(tag: List[str] = fastapi.Query(...), user=fastapi.Depends(get_user_from_token)):
    return tag


@app.delete('/')
async def delete(uuid: str = fastapi.Query(...), user=fastapi.Depends(get_user_from_token)):
    try:
        meta_path = pathlib.Path(DATA_PATH, user, f"{uuid}_meta.yml")
        with open(meta_path, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
        path = data.get('path', None)
        if path is None:
            raise Exception("path is empty")
        file_path = pathlib.Path(DATA_PATH, path)
        if not file_path.exists():
            raise Exception(f"{path} not exist")
        os.remove(meta_path)
        os.remove(file_path)
    except Exception as e:
        raise fastapi.HTTPException(fastapi.status.HTTP_404_NOT_FOUND)
    return {"uuid": uuid}
