from FastAPIRouterWrapper import FastAPIRouterWrapper

__all__ = ["MemeRouter"]

class MemeRouter(FastAPIRouterWrapper):
    from .app import app, statics
    from .crud import startup, shutdown
    app = app
    statics = statics
    startup_handler = [startup]
    shutdown_handler = [shutdown]
