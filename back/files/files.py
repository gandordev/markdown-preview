from pathlib import Path

from MagicConvert import MagicConvert
from puremagic.main import PureError

CONVERTER = MagicConvert()
DOWNLOAD_PATH = Path.home() / "Downloads"


def convert_file_to_md(*, source: str, folder: str = "", file_name = "") -> str:
    """
    Convert any file to Markdown and save it.

    Parameters
    ----------
    source : str
        Path to the source file
    folder : str, optional
        Folder to save the converted file, by default ""
    file_name : str, optional
        Name of the MD file, by default ""

    Returns
    -------
    str
        Message including the path to the saved Markdown file

    Raises
    ------
    PureError
        Raised when the file format is incorrect
    Exception
        Raised when an error occurs during conversion
    Exception
        Raised when an error occurs during saving
    """
    title = source.replace("\\", "/").split('/')[-1]

    # Convert
    try:
        res = CONVERTER.magic(source)
    except PureError:
        raise PureError(
            f"Error al convertir el archivo '{title}' a MarkDown: Formato de archivo incorrecto."
            "\nEjemplo: el archivo es .txt y se ha indicado como .docx"
        )
    except Exception as e:
        raise Exception(f"Ha ocurrido un error al intentar convertir el archivo '{title}' a MarkDown: {e}")

    # Save
    try:
        response = _save_file_to_folder(
            content=res.text_content,
            file_name=title if not file_name else file_name,
            folder=Path(folder) if folder and Path(folder).is_dir() else None,
        )
    except Exception as e:
        raise Exception(f"Ha ocurrido un error al guardar el archivo: {e}")

    return response["content"]

## Private methods ##
def _save_file_to_folder(*, content: str, file_name: str, folder: Path | None = None) -> dict[str, str]:
    """
    Save content to a file in the specified folder.

    Parameters
    ----------
    content : str
        Content to be saved in the file
    file_name : str
        Name of the file to save
    folder : Path | None, optional
        Folder to save the file, by default is the Downloads folder

    Returns
    -------
    dict[str, str]
        Dictionary with a message about the saved file
    """
    if folder is None:
        folder = DOWNLOAD_PATH

    file_path = f"{folder}/{file_name}.md"

    # Write
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception:
        raise

    return {"content": f"Archivo guardardado correctamente en la ruta {file_path}"}
