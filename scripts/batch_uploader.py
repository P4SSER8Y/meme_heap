from prompt_toolkit import prompt
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.completion import WordCompleter
import click
import httpx
import os
from pathlib import Path
from queue import Queue
import cv2
import threading
import asyncio

q = Queue()
loop = None
e = asyncio.Event()
url = ""
token = ""


def thread_preview():
    while True:
        img = q.get(True)
        if img is None:
            break
        h = img.shape[0]
        w = img.shape[1]
        if w > h:
            img = cv2.resize(img, [512, h * 512 // w])
        else:
            img = cv2.resize(img, [w * 512 // h, 512])
        cv2.imshow('preview', img)
        cv2.waitKey(1)
    cv2.destroyAllWindows()


def preview_and_get_tags(path):
    prompt
    print(f"{path}")
    try:
        tags = httpx.get(url=f"{url}tag/", params={'token': token}).json()
        tags = [x['tag'] for x in tags]
        img = cv2.imread(str(path))
        if img is None:
            return None
        q.put(img)
        return(prompt("Tags>> ", completer=WordCompleter(tags)))
    except Exception as e:
        print(f"{path} is invalid: {e}")
        return None


def start_loop():
    print("hello")
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    e.clear()
    loop.run_until_complete(e.wait())
    print('goodbye')


def stop_loop():
    async def f():
        e.set()
    asyncio.run_coroutine_threadsafe(f(), loop)


async def push(path, tags):
    global url
    global token
    try:
        async with httpx.AsyncClient() as client:
            ret = await client.post(f"{url}meme/", params={'token': token}, data={"tags": tags}, files={'file': open(path, 'rb')})
            print(f"push {path} {ret.is_success}")
            await client.aclose()
            if ret.is_success:
                os.remove(path)
    except Exception as e:
        print(f"wtf?? {e}")


@click.command()
@click.argument('base', type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True))
def main(base):
    global url
    global token
    url = prompt('URL=? ')
    token = prompt('token=? ')
    print(f"reading {base}")
    prv = threading.Thread(target=thread_preview)
    t = threading.Thread(target=start_loop)
    prv.start()
    t.start()
    try:
        for root, _, files in os.walk(base):
            for file in files:
                tags: str = preview_and_get_tags(Path(root, file))
                if (tags is not None) and (len(tags.strip()) > 0):
                    asyncio.run_coroutine_threadsafe(push(Path(root, file), tags), loop)
    finally:
        stop_loop()
        q.put(None)
        prv.join()


if __name__ == "__main__":
    main()
