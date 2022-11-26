from fastapi import APIRouter
from pathlib import Path
from typing import Coroutine, Dict, List

class FastAPIRouterWrapper():
    app: APIRouter = None
    statics: Dict[str, Path] = []
    startup_handler: List[Coroutine] = []
    shutdown_handler: List[Coroutine] = []
