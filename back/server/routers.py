import tempfile
from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from ..files import convert_file_to_md

STATIC_FILES = Path().cwd() / "front" / "static"


root = APIRouter(prefix="", tags=["root"])

@root.get("/")
async def index() -> FileResponse:
    """
    Serve the index.html file.

    Returns
    -------
    FileResponse
        The index.html file as response
    """
    return FileResponse(STATIC_FILES / "index.html")


@root.post("/api/convert")
async def convert_to_md(files: List[UploadFile]) -> dict[str, list[str]]:
    """
    Convert uploaded files to Markdown.

    Parameters
    ----------
    files : List[UploadFile]
        List of uploaded files to convert

    Returns
    -------
    dict[str, list[str]]
        Dictionary with list of converted Markdown contents
    """
    converted = []

    for file in files:
        # Create temp file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file.filename
        ) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Convert to md
        md_content = convert_file_to_md(
            source=tmp_path,
            file_name=str(file.filename).replace("\\", "/").split("/")[-1],
        )

        # Save to response
        converted.append(md_content)

    return {"converted": converted}


## WebSocket for live reload ##
@root.websocket("/ws/reload")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for live reload.

    Parameters
    ----------
    websocket : WebSocket
        The websocket connection
    """
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
