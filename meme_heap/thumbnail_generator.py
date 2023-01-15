from PIL import Image
from loguru import logger
from pathlib import Path

async def generate_thumbnail(src: str | Path, dst: str | Path):
    try:
        img = Image.open(src)
        img.seek(0)
        img = img.convert('RGB')
        logger.debug(f'processing {src}: HxV={img.width}x{img.height}')
        if img.width >= 256:
            height = img.height * 256 // img.width
            img = img.resize([256, height])
            logger.debug(f'resize to {img.width}x{img.height}')
        img.save(dst)
        logger.debug("saved to {}", dst)
        return True
    except Exception as e:
        logger.exception('nani?')
        return False

