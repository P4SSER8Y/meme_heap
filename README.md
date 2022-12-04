Meme Heap
===========
[![CI](https://github.com/P4SSER8Y/meme_heap/actions/workflows/ocean.yaml/badge.svg)](https://github.com/P4SSER8Y/meme_heap/actions/workflows/ocean.yaml)

A storage for memes, with features:
- multiple users
- search by tag(s)
- add or remove memes
- add or remove tags
- auto generate thumbnails if file-type supported
- CI test since Python 3.8

Usage
-----------
+ install
    - `poetry install`
    - build UI
        + `cd ./meme_ui`
        + `pnpm install`
        + `pnpm build`
+ run
    - `poetry run python main.py`
    - `poetry run uvicorn entry:app`

Environment Variables
---------------------
+ MEME_DATA_PATH
    + Description: data storage path
    + Default: `./data`
+ MEME_DB_ADMIN
    + Description: default admin user name on initialization
    + Default: `admin`
+ MEME_DB_ADMIN_TOKEN
    + Description: default admin token on initialization
    + Default: `admin`
+ MEME_DB_URL:
    + Description: database URL, see [SQLAlchemy Engine Docs](https://www.osgeo.cn/sqlalchemy/core/engines.html)
    + Default: `sqlite:///${MEME_DATA_PATH}/sqlite.db`
+ MEME_TOKEN_SALT:
    + Description: salt of token
    + Default: `memeMEME1v131v13`
+ UI_PATH:
    + Description: frontend UI files path
    + Default: `./meme_ui/dist`
