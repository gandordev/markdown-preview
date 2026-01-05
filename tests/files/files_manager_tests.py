import sys
from pathlib import Path

# Add parent directory to sys.path to allow imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from back.files import convert_file_to_md

CUR_DIR = Path().cwd()


## test_convert_file_to_md_returns_PureError ##
print(convert_file_to_md(source=f"{CUR_DIR}/files/Códigos_html_y_css_formulariolula.docx"))

## test_convert_file_pdf_to_md_returns_dict_with_pdf ##
print(convert_file_to_md(source=f"{CUR_DIR}/files/Códigos_html_y_css_formulariolula.docx.pdf"))

## test_convert_file_word_to_md_returns_dict_with_word ##
print(convert_file_to_md(source=f"{CUR_DIR}/files/TF4ef8e72c-1067-4295-ad89-c8a0b6e589af3bffe0c4_wac-d4759bd8ab99.docx"))
