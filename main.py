import uvicorn
from meme_heap import app

if __name__ == "__main__":
    uvicorn.run(app=app, host='127.0.0.1')
