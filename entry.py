from meme_heap import app as meme
from fastapi import FastAPI

app = FastAPI()
app.include_router(meme, prefix='/meme')
