from pathlib import Path
from typing import Union
from pypdf import PdfReader
from pypdf.errors import PdfReadError

def extract_text_from_pdf(file_path: Union[str, Path]) -> str:
    """
    Extract all text content from a PDF file.

    Args:
        file_path (Union[str, Path]): Path to the PDF file.

    Returns:
        str: Extracted text from all pages in the PDF, concatenated.
             If the PDF has no extractable text (e.g. scanned image/blank),
             an empty string is returned.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        IsADirectoryError: If the provided path points to a directory.
        ValueError: If the file is not a valid PDF or is corrupted.
        PermissionError: If there are insufficient permissions to read the file.
    """
    path = Path(file_path)

    # Explicit directory check for consistent cross-platform raising of IsADirectoryError
    if path.is_dir():
        raise IsADirectoryError(f"The path '{path}' is a directory, not a file.")

    if not path.exists():
        raise FileNotFoundError(f"The PDF file '{path}' does not exist.")

    try:
        reader = PdfReader(path)
        extracted_pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_pages.append(text)
        return "\n\n".join(extracted_pages)
    except PdfReadError as e:
        raise ValueError(f"Failed to read PDF file '{path}': {e}") from e
    except Exception as e:
        if isinstance(e, PermissionError) or "Permission" in str(e):
            raise PermissionError(f"Permission denied accessing PDF file: {path}") from e
        raise ValueError(f"The file '{path}' is not a valid or supported PDF file.") from e
