from pathlib import Path
from typing import Union, Tuple
from PIL import Image, UnidentifiedImageError

def resize_image(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    dimensions: Tuple[int, int],
) -> None:
    """
    Resize an image to the specified width and height.

    Args:
        input_path (Union[str, Path]): Path to the input image file.
        output_path (Union[str, Path]): Path where the resized image will be saved.
        dimensions (Tuple[int, int]): A tuple of (width, height) for the target size.

    Returns:
        None

    Raises:
        FileNotFoundError: If the input file does not exist.
        IsADirectoryError: If either input or output path is a directory.
        ValueError: If dimensions are invalid, or if the file is not a supported/valid image.
        PermissionError: If there are insufficient permissions to read/write files.
    """
    in_path = Path(input_path)
    out_path = Path(output_path)

    # Explicit directory checks for consistent cross-platform raising of IsADirectoryError
    if in_path.is_dir():
        raise IsADirectoryError(f"The input path '{in_path}' is a directory, not a file.")
    if out_path.is_dir():
        raise IsADirectoryError(f"The output path '{out_path}' is a directory, not a file.")

    if not in_path.exists():
        raise FileNotFoundError(f"The input file '{in_path}' does not exist.")

    # Validate dimensions
    if not isinstance(dimensions, tuple) or len(dimensions) != 2:
        raise ValueError("Dimensions must be a tuple of (width, height).")

    width, height = dimensions
    if not isinstance(width, int) or not isinstance(height, int):
        raise ValueError("Dimensions (width and height) must be integers.")

    if width <= 0 or height <= 0:
        raise ValueError("Dimensions (width and height) must be positive integers greater than zero.")

    try:
        with Image.open(in_path) as img:
            # Resize using high-quality LANCZOS filter
            resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Ensure the output parent directory exists
            out_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the resized image, preserving format if possible or deriving from extension
            resized_img.save(out_path)
    except UnidentifiedImageError as e:
        raise ValueError(f"The file '{in_path}' is not a supported image or is corrupted.") from e
    except OSError as e:
        # PIL can raise OSError for write/read issues or unsupported operations
        if "Permission" in str(e) or "permission" in str(e):
            raise PermissionError(f"Permission denied accessing files.") from e
        raise ValueError(f"Failed to process image file: {e}") from e
