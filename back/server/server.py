import uvicorn

PORT = 8000
HOST = "0.0.0.0"
RELOAD = True


def run():
    uvicorn.run(
        "back.server.config:app",  # Ruta al objeto app
        host=HOST,
        port=PORT,
        reload=RELOAD,
        reload_dirs=["back", "front"],
        # reload_includes=["*"]
    )
