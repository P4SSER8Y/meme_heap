from FastAPIRouterWrapper import FastAPIRouterWrapper

__all__ = ["MemeRouter"]

class MemeRouter(FastAPIRouterWrapper):
    from .app import app, statics
    from .db import startup, shutdown
    app = app
    statics = statics
    startup_handler = [startup]
    shutdown_handler = [shutdown]
