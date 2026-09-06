import hashlib
from pathlib import Path
from typing import Union

def calculate_sha256(file_path: Union[str, Path], chunk_size: int = 65536) -> str:
    """
    Calculate the SHA-256 cryptographic hash of a file.

    Args:
        file_path (Union[str, Path]): Path to the file to be hashed.
        chunk_size (int): Size of chunks to read from the file in bytes (default: 64KB).

    Returns:
        str: The 64-character hexadecimal SHA-256 digest of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        IsADirectoryError: If the provided path points to a directory.
        PermissionError: If there are insufficient permissions to read the file.
    """
    path = Path(file_path)

    # Explicit directory check for consistent cross-platform raising of IsADirectoryError
    if path.is_dir():
        raise IsADirectoryError(f"The path '{path}' is a directory, not a file.")

    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(chunk_size), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()
