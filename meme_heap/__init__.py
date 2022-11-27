from FastAPIRouterWrapper import FastAPIRouterWrapper

__all__ = ["MemeRouter"]

class MemeRouter(FastAPIRouterWrapper):
    from .app import app, statics_handler
    from .crud import startup, shutdown
    app = app
    statics_handler = [statics_handler]
    startup_handler = [startup]
    shutdown_handler = [shutdown]
