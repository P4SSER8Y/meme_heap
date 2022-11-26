Meme Heap
===========

A storage for memes, with features:
- multiple users
- search by tag(s)
- add or remove memes
- add or remove tags
- auto generate thumbnails if file-type supported

Usage
-----------
+ install
    - `poetry install`
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
