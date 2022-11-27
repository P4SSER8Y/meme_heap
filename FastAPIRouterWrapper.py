
class FastAPIRouterWrapper():
    from fastapi import APIRouter, FastAPI
    from typing import Callable, Coroutine, List

    app: APIRouter = None
    statics_handler: List[Callable[[FastAPI, str], None]] = []
    startup_handler: List[Coroutine] = []
    shutdown_handler: List[Coroutine] = []
