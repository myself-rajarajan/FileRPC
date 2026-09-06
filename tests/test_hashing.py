import unittest
import tempfile
import os
from pathlib import Path
from src.processing.hashing import calculate_sha256

class TestHashing(unittest.TestCase):
    def test_calculate_sha256_known_content(self):
        """Test hashing a known text file with a known expected SHA-256 hash."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            content = b"Hello, FileRPC!"
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Expected SHA-256 hash of "Hello, FileRPC!"
            expected_hash = "58c9a11c4bba49a568202d08e375e429b391e6147ef1c26b247b83b8734236cc"
            actual_hash = calculate_sha256(tmp_path)
            self.assertEqual(actual_hash, expected_hash)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_calculate_sha256_empty_file(self):
        """Test hashing an empty file."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Expected SHA-256 hash of empty content
            expected_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            actual_hash = calculate_sha256(tmp_path)
            self.assertEqual(actual_hash, expected_hash)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_calculate_sha256_missing_file(self):
        """Test that a missing/non-existent file raises FileNotFoundError."""
        non_existent_file = "this_file_does_not_exist_12345.txt"
        with self.assertRaises(FileNotFoundError):
            calculate_sha256(non_existent_file)

    def test_calculate_sha256_directory(self):
        """Test that trying to hash a directory raises IsADirectoryError."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            with self.assertRaises(IsADirectoryError):
                calculate_sha256(tmp_dir)

if __name__ == "__main__":
    unittest.main()
