from pathlib import Path

import pytest
from pypdf import PdfWriter
from pypdf.generic import (
    NameObject,
    DictionaryObject,
    DecodedStreamObject,
)

from src.processing.pdf_extraction import extract_text_from_pdf


def create_test_pdf(path: Path, text: str = "Hello FileRPC"):
    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)

    font = DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
    })

    font_ref = writer._add_object(font)

    resources = DictionaryObject({
        NameObject("/Font"): DictionaryObject({
            NameObject("/F1"): font_ref
        })
    })

    page[NameObject("/Resources")] = resources

    stream = DecodedStreamObject()
    stream.set_data(
        f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
    )

    page[NameObject("/Contents")] = writer._add_object(stream)

    with open(path, "wb") as file:
        writer.write(file)


def test_extract_text(tmp_path):
    pdf = tmp_path / "test.pdf"
    create_test_pdf(pdf, "Hello FileRPC")

    result = extract_text_from_pdf(pdf)

    assert "Hello FileRPC" in result


def test_extract_text_multiple_pages(tmp_path):
    pdf = tmp_path / "test.pdf"

    writer = PdfWriter()

    for text in ["Page One", "Page Two"]:
        page = writer.add_blank_page(width=612, height=792)

        font = DictionaryObject({
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject("/Helvetica"),
        })

        font_ref = writer._add_object(font)

        page[NameObject("/Resources")] = DictionaryObject({
            NameObject("/Font"): DictionaryObject({
                NameObject("/F1"): font_ref
            })
        })

        stream = DecodedStreamObject()
        stream.set_data(
            f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
        )

        page[NameObject("/Contents")] = writer._add_object(stream)

    with open(pdf, "wb") as file:
        writer.write(file)

    result = extract_text_from_pdf(pdf)

    assert "Page One" in result
    assert "Page Two" in result


def test_missing_pdf(tmp_path):
    pdf = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf(pdf)


def test_directory_path(tmp_path):
    with pytest.raises(IsADirectoryError):
        extract_text_from_pdf(tmp_path)


def test_invalid_pdf(tmp_path):
    pdf = tmp_path / "invalid.pdf"
    pdf.write_text("This is not a PDF")

    with pytest.raises(ValueError):
        extract_text_from_pdf(pdf)