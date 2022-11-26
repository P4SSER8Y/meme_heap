from typing import List
from meme_heap import MemeRouter
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from FastAPIRouterWrapper import FastAPIRouterWrapper

routers: List[FastAPIRouterWrapper] = [MemeRouter]

app = FastAPI()

for item in routers:
    app.include_router(item.app, prefix='/meme')
    for key in item.statics.keys():
        app.mount(f'/meme{key}', StaticFiles(directory=item.statics[key]))


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
