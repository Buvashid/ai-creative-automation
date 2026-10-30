from pathlib import Path

import pytest
from PIL import Image

from app.template_renderer import (
    _ShapedFont,
    _find_font,
    render_creative,
    render_placeholder,
)


def creative_copy() -> dict[str, str]:
    return {
        "creative_id": "creative-1",
        "product": "Credit Card",
        "headline": "Build your money habits",
        "body": "Simple tools for your everyday planning.",
        "offer": "Verified offer",
        "language": "English",
        "disclaimer": "Fictional demonstration material - not financial advice.",
    }


def test_render_creative_creates_1080_png_and_output_directory(tmp_path: Path):
    output_dir = tmp_path / "nested" / "output"

    output_path = render_creative(creative_copy(), output_dir)

    assert output_path == output_dir / "creative-1.png"
    assert output_path.exists()
    with Image.open(output_path) as image:
        assert image.size == (1080, 1080)
        assert image.format == "PNG"


def test_render_placeholder_remains_available(tmp_path: Path):
    output_path = render_placeholder(tmp_path / "creative.png")

    assert output_path.exists()


def test_render_creative_rejects_missing_input():
    copy_data = creative_copy()
    del copy_data["offer"]

    with pytest.raises(ValueError, match="Missing required copy fields: offer"):
        render_creative(copy_data)


def test_render_creative_rejects_empty_input():
    copy_data = creative_copy()
    copy_data["headline"] = " "

    with pytest.raises(ValueError, match="Copy field 'headline' cannot be empty"):
        render_creative(copy_data)


def test_render_creative_rejects_unsafe_creative_id(tmp_path: Path):
    copy_data = creative_copy()
    copy_data["creative_id"] = "../outside"

    with pytest.raises(ValueError, match="filename-safe"):
        render_creative(copy_data, tmp_path)


def test_render_creative_rejects_unsupported_language(tmp_path: Path):
    copy_data = creative_copy()
    copy_data["language"] = "French"

    with pytest.raises(ValueError, match="Unsupported language 'French'"):
        render_creative(copy_data, tmp_path)


def test_render_creative_rejects_text_that_cannot_fit(tmp_path: Path):
    copy_data = creative_copy()
    copy_data["body"] = " ".join(["Very long body text"] * 500)

    with pytest.raises(ValueError, match="cannot fit"):
        render_creative(copy_data, tmp_path)


@pytest.fixture
def devanagari_font(monkeypatch):
    font_path = Path(r"C:\Windows\Fonts\Nirmala.ttc")
    if not font_path.is_file():
        pytest.skip("Nirmala.ttc is required for Devanagari rendering tests")
    monkeypatch.setenv("PAISAPATH_DEVANAGARI_FONT_PATH", str(font_path))
    return font_path


@pytest.mark.parametrize(
    ("language", "text"),
    [
        ("Hindi", "निवेश की बुनियादी बातें समझें"),
        ("Marathi", "गुंतवणुकीच्या मूलभूत गोष्टी जाणून घ्या"),
    ],
)
def test_devanagari_shaping_returns_positioned_glyphs(
    language, text, devanagari_font
):
    font = _ShapedFont(devanagari_font, 34)

    infos, positions = font.shape(text)

    assert infos
    assert len(infos) == len(positions)
    assert any(position.x_advance > 0 for position in positions)
    assert font.measure(text) > 0


def test_devanagari_conjunct_is_shaped_to_a_ligature(devanagari_font):
    font = _ShapedFont(devanagari_font, 34)

    infos, _ = font.shape("क्ष")

    assert len(infos) == 1


@pytest.mark.parametrize(
    ("language", "text"),
    [
        ("Hindi", "निवेश की बुनियादी बातें समझें"),
        ("Marathi", "गुंतवणुकीच्या मूलभूत गोष्टी जाणून घ्या"),
    ],
)
def test_render_creative_shapes_devanagari_text(
    language, text, tmp_path: Path, devanagari_font
):
    copy_data = {
        "creative_id": f"{language.lower()}-shaped",
        "product": text,
        "headline": text,
        "body": text,
        "offer": "केवळ प्रात्यक्षिक उदाहरण ऑफर",
        "language": language,
        "disclaimer": "ही केवळ काल्पनिक प्रात्यक्षिक सामग्री आहे. हा आर्थिक सल्ला नाही.",
    }

    output_path = render_creative(copy_data, tmp_path)

    with Image.open(output_path) as image:
        assert image.size == (1080, 1080)
        assert image.format == "PNG"
