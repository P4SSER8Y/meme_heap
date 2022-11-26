import uvicorn

if __name__ == "__main__":
    uvicorn.run(app="entry:app", host='127.0.0.1', reload=True)
