import unittest
import tempfile
from pathlib import Path
from PIL import Image
from src.processing.resizing import resize_image

class TestImageResizing(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = Path(self.temp_dir.name)
        
        # Create a valid source image (e.g., 100x100 red square)
        self.src_image_path = self.temp_dir_path / "test_source.png"
        img = Image.new("RGB", (100, 100), color="red")
        img.save(self.src_image_path)
        
        # Output path
        self.dest_image_path = self.temp_dir_path / "test_output.png"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_resize_image_success(self):
        """Test successful image resizing to standard dimensions."""
        dimensions = (50, 50)
        resize_image(self.src_image_path, self.dest_image_path, dimensions)
        
        # Verify output exists
        self.assertTrue(self.dest_image_path.exists())
        
        # Verify dimensions of output image
        with Image.open(self.dest_image_path) as out_img:
            self.assertEqual(out_img.size, dimensions)

    def test_resize_image_dimensions(self):
        """Test that different combinations of output dimensions work correctly."""
        dimensions = (120, 80)
        resize_image(self.src_image_path, self.dest_image_path, dimensions)
        self.assertTrue(self.dest_image_path.exists())
        with Image.open(self.dest_image_path) as out_img:
            self.assertEqual(out_img.size, dimensions)

    def test_resize_image_missing_input(self):
        """Test that attempting to resize a missing file raises FileNotFoundError."""
        non_existent_file = self.temp_dir_path / "does_not_exist.png"
        with self.assertRaises(FileNotFoundError):
            resize_image(non_existent_file, self.dest_image_path, (50, 50))

    def test_resize_image_is_directory(self):
        """Test that using directories as paths raises IsADirectoryError."""
        # Input path is a directory
        with self.assertRaises(IsADirectoryError):
            resize_image(self.temp_dir_path, self.dest_image_path, (50, 50))
            
        # Output path is a directory
        with self.assertRaises(IsADirectoryError):
            resize_image(self.src_image_path, self.temp_dir_path, (50, 50))

    def test_resize_image_invalid_dimensions(self):
        """Test that invalid dimensions raise ValueError."""
        invalid_cases = [
            (0, 50),
            (50, 0),
            (-50, 50),
            (50, -50),
            ("50", 50),
            (50, "50"),
            (50,), # too short
            (50, 50, 50), # too long
            "not-a-tuple",
        ]
        for dims in invalid_cases:
            with self.subTest(dims=dims):
                with self.assertRaises(ValueError):
                    resize_image(self.src_image_path, self.dest_image_path, dims) # type: ignore

    def test_resize_image_unsupported_or_corrupt_input(self):
        """Test that trying to resize an invalid/unsupported/corrupted file raises ValueError."""
        corrupt_file_path = self.temp_dir_path / "corrupt.png"
        # Write some non-image text content
        with open(corrupt_file_path, "w") as f:
            f.write("This is definitely not a PNG image file!")
            
        with self.assertRaises(ValueError):
            resize_image(corrupt_file_path, self.dest_image_path, (50, 50))

if __name__ == "__main__":
    unittest.main()
