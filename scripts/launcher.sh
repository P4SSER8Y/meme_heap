#!/bin/sh

pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple
pip config set global.trusted-host mirrors.cloud.tencent.com
pip install poetry
poetry lock --no-update
poetry install
poetry run python main.py
