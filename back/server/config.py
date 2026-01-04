
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .routers import root

## Server parameters ##
API_CONFIG = {
    "title": "Markdown Preview",
    "description": "Convert any file to MD or format an existing MD.",
    "version": "0.1.0",
    "contact": {"name": "gandordev", "url": "https://github.com/gandordev"}
}


# Initialize app
app = FastAPI(**API_CONFIG)

# Include routers in app
app.include_router(root)

# Mount static files
# TODO: Modify structure to insert this folders into static
app.mount("/styles", StaticFiles(directory="front/styles"), name="styles")
app.mount("/scripts", StaticFiles(directory="front/scripts"), name="scripts")

# Manage exceptions, to return a JSON
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, e: Exception):
    return JSONResponse({"message": "Internal server error"}, 500)
