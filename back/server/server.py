import uvicorn
from uvicorn import Config, Server

from .config import app

PORT = 8000
HOST = "0.0.0.0"
RELOAD = True

def get_server_config():
    return Config(app=app, host=HOST, port=PORT, reload=RELOAD)


def run():
    uvicorn.run(
        "back.server.config:app",  # Ruta al objeto app
        host=HOST,
        port=PORT,
        reload=RELOAD,
        reload_dirs=["back", "front"],  # Detecta cambios en estas carpetas
        reload_includes=["*"]
    )
    # server_config = get_server_config()
    # server = Server(server_config)
    # server.run()
