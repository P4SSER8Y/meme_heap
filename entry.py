import meme_heap
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(meme_heap.app, prefix='/meme')
for key in meme_heap.statics.keys():
    app.mount(f'/meme{key}', StaticFiles(directory=meme_heap.statics[key]))
