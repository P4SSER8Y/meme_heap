from typing import List
from meme_heap import MemeRouter
from fastapi import FastAPI
from FastAPIRouterWrapper import FastAPIRouterWrapper
from fastapi.testclient import TestClient
from fastapi import status

routers: List[FastAPIRouterWrapper] = [MemeRouter]

app = FastAPI()

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

#####################################################################

client = TestClient(app)

def test_smoke():
    response = client.get('/meme')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
