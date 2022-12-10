import uvicorn
from LoggerInitialization import init_logging
import os
from loguru import logger

if __name__ == "__main__":
    logger.info('hello world')
    if os.environ.get('DEVELOP', None):
        develop_mode = True
    else:
        develop_mode = False
    logger.info(f"develop mode: {develop_mode}")
    host=os.environ.get('MEME_HOST', '127.0.0.1')
    port=int(os.environ.get('MEME_PORT', '8000'))
    cfg = uvicorn.Config(app="entry:app", host=host, port=port, reload=develop_mode)
    init_logging()
    server = uvicorn.Server(cfg)
    server.run()
    logger.info('goodbye')
