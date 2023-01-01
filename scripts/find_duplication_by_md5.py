from hashlib import md5
from typing import Dict, List
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit import print_formatted_text as print
import click
import os
import pathlib
import httpx
from urllib.parse import urljoin

url = ""
token = ""


@click.command()
@click.argument('base', type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True))
def main(base):
    global url
    global token
    url = prompt("url=? ")
    token =prompt("token=? ")
    m: Dict[str, List[str]] = {}
    with ProgressBar() as pb:
        for item in pb(os.listdir(base)):
            path = pathlib.Path(base, item)
            if not path.is_file():
                continue
            with open(path, 'rb') as file:
                raw = file.read()
                hash = md5(raw).hexdigest()
                if hash in m.keys():
                    m[hash].append(path.stem)
                else:
                    m[hash] = [path.stem]
    for hash in m.keys():
        if len(m[hash]) > 1:
            ret = httpx.post(f"{url}meme/merge/", json={"token": token, "uuids": m[hash]})
            print(f"{hash}: {m[hash]} --- {ret.is_success}")


if __name__ == "__main__":
    main()
