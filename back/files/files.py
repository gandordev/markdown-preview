from pathlib import Path

from MagicConvert import MagicConvert
from puremagic.main import PureError

CONVERTER = MagicConvert()
HOME_PATH = Path.home() / "Downloads"


def convert_file_to_md(*, source: str, folder: str = "", file_name = "") -> str:
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

#region private
def _save_file_to_folder(*, content: str, file_name: str, folder: Path | None = None) -> dict[str, str]:
    if folder is None:
        folder = HOME_PATH

    file_path = f"{folder}/{file_name}.md"

    # Write
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception:
        raise

    return {"content": f"Archivo guardardado correctamente en la ruta {file_path}"}
#endregion



