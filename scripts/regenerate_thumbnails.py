import click
from meme_heap.thumbnail_generator import generate_thumbnail
import os
from pathlib import Path
import asyncio


async def f(src, dst):
    await generate_thumbnail(src, dst)
    print(f"{src} => {dst}")


async def g(tasks):
    await asyncio.gather(*tasks)


@click.command()
@click.argument('base', type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True))
def main(base):
    users = os.listdir(Path(base, 'raw'))
    tasks = []
    for user in users:
        raw = Path(base, 'raw', user)
        thumbnail = Path(base, 'thumbnail', user)
        for file in os.listdir(raw):
            src = Path(raw, file)
            dst = Path(thumbnail, src.stem + '.jpg')
            tasks.append(generate_thumbnail(src, dst))
    asyncio.run(g(tasks))


if __name__ == "__main__":
    main()

