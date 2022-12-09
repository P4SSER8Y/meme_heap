from typing import List
from meme_heap import MemeRouter
from fastapi import FastAPI
from FastAPIRouterWrapper import FastAPIRouterWrapper
import os

routers: List[FastAPIRouterWrapper] = [MemeRouter]

is_dev_mode = os.environ.get('DEVELOP', None)
if is_dev_mode:
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)

for item in routers:
    app.include_router(item.app, prefix='/meme')
    for func in item.statics_handler:
        func(app, '/meme')


@app.on_event("startup")
async def startup():
    for item in routers:
        for func in item.startup_handler:
            await func()


@app.on_event("shutdown")
async def shutdown():
    for item in routers:
        for func in item.shutdown_handler:
            await func()
