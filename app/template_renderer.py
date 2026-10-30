"""Render structured creative copy as branded PNG advertisements."""

import os
from collections.abc import Mapping
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, features

from app.config import CANVAS_SIZE, OUTPUT_DIR

REQUIRED_FIELDS = ("creative_id", "headline", "body", "offer", "language", "disclaimer")
SUPPORTED_LANGUAGES = {"English", "Hindi", "Marathi"}
FONT_ENVIRONMENT_VARIABLE = "PAISAPATH_FONT_PATH"
DEVANAGARI_FONT_ENVIRONMENT_VARIABLE = "PAISAPATH_DEVANAGARI_FONT_PATH"
WINDOWS_FONT_DIR = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
FONT_CANDIDATES = ("arial.ttf", "calibri.ttf", "segoeui.ttf")
DEVANAGARI_FONT_CANDIDATES = ("NirmalaUI.ttf", "Nirmala.ttf", "mangal.ttf")


def _find_font(language: str) -> Path:
    environment_variable = (
        DEVANAGARI_FONT_ENVIRONMENT_VARIABLE
        if language in {"Hindi", "Marathi"}
        else FONT_ENVIRONMENT_VARIABLE
    )
    configured_path = os.environ.get(environment_variable)
    if configured_path:
        font_path = Path(configured_path)
        if font_path.is_file():
            return font_path
        raise ValueError(
            f"{environment_variable} points to a missing font file: {font_path}"
        )

    candidates = (
        DEVANAGARI_FONT_CANDIDATES
        if language in {"Hindi", "Marathi"}
        else FONT_CANDIDATES
    )
    for candidate in candidates:
        font_path = WINDOWS_FONT_DIR / candidate
        if font_path.is_file():
            return font_path

    if language in {"Hindi", "Marathi"}:
        raise ValueError(
            "No Windows Devanagari font was found. Install Nirmala UI or Mangal, "
            f"or set {DEVANAGARI_FONT_ENVIRONMENT_VARIABLE} to a .ttf file."
        )
    raise ValueError(
        f"No usable font was found. Set {FONT_ENVIRONMENT_VARIABLE} to a .ttf file."
    )


def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Wrap text by measured pixels, including long unbroken words."""
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            if font.getlength(candidate) <= max_width:
                current = candidate
                continue
            if current:
                lines.append(current)
            current = ""
            for character in word:
                candidate = current + character
                if current and font.getlength(candidate) > max_width:
                    lines.append(current)
                    current = character
                else:
                    current = candidate
        if current:
            lines.append(current)
    return lines


def _load_font(font_path: Path, size: int) -> ImageFont.FreeTypeFont:
    """Load a font with RAQM shaping when this Pillow build provides it.

    RAQM improves complex-script layout where available, but rendered Hindi and
    Marathi still require visual inspection because shaping support depends on
    the installed Pillow build and font.
    """
    layout_engine = getattr(ImageFont, "Layout", None)
    if (
        layout_engine is not None
        and hasattr(layout_engine, "RAQM")
        and features.check("raqm")
    ):
        try:
            return ImageFont.truetype(
                font_path,
                size,
                layout_engine=layout_engine.RAQM,
            )
        except (OSError, ValueError):
            pass
    return ImageFont.truetype(font_path, size)


def _fit_text(
    text: str,
    font_path: Path,
    max_width: int,
    max_height: int,
    largest_size: int,
    smallest_size: int,
) -> tuple[ImageFont.FreeTypeFont, list[str], int]:
    for size in range(largest_size, smallest_size - 1, -2):
        font = _load_font(font_path, size)
        lines = _wrap_text(text, font, max_width)
        font_box = font.getbbox("Ag")
        line_height = font_box[3] - font_box[1] + 8
        if len(lines) * line_height <= max_height:
            return font, lines, line_height
    raise ValueError("Creative text cannot fit in the advertisement layout.")


def _draw_text_block(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_path: Path,
    position: tuple[int, int],
    max_width: int,
    max_height: int,
    largest_size: int,
    smallest_size: int,
    fill: str,
) -> int:
    font, lines, line_height = _fit_text(
        text,
        font_path,
        max_width,
        max_height,
        largest_size,
        smallest_size,
    )
    x, y = position
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y


def render_creative(
    copy_data: Mapping[str, object],
    output_dir: Path = OUTPUT_DIR,
) -> Path:
    """Render one structured creative and return its PNG path."""
    missing_fields = [field for field in REQUIRED_FIELDS if field not in copy_data]
    if missing_fields:
        raise ValueError(f"Missing required copy fields: {', '.join(missing_fields)}")

    for field in REQUIRED_FIELDS:
        value = copy_data[field]
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValueError(f"Copy field '{field}' cannot be empty")

    creative_id = str(copy_data["creative_id"])
    if Path(creative_id).name != creative_id:
        raise ValueError("creative_id must be a simple filename-safe value")

    language = copy_data["language"]
    if not isinstance(language, str) or language not in SUPPORTED_LANGUAGES:
        supported_languages = ", ".join(sorted(SUPPORTED_LANGUAGES))
        raise ValueError(
            f"Unsupported language '{language}'. Supported languages: "
            f"{supported_languages}"
        )

    font_path = _find_font(language)
    headline = str(copy_data["headline"])
    body = str(copy_data["body"])
    offer = str(copy_data["offer"])
    disclaimer = str(copy_data["disclaimer"])
    product = str(copy_data.get("product", headline))

    image = Image.new("RGB", CANVAS_SIZE, "#F7F1E5")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1080, 270), fill="#102A43")
    draw.rectangle((0, 270, 1080, 282), fill="#D9A441")

    draw.text((72, 58), "PaisaPath", font=_load_font(font_path, 54), fill="#F7F1E5")
    draw.text((72, 145), product, font=_load_font(font_path, 26), fill="#D9A441")
    draw.text(
        (900, 70),
        language,
        font=_load_font(font_path, 24),
        fill="#F7F1E5",
        anchor="ra",
    )

    content_x = 72
    content_width = 936
    y = 340
    y = _draw_text_block(
        draw, headline, font_path, (content_x, y), content_width, 190, 64, 30, "#102A43"
    )
    y += 24
    y = _draw_text_block(
        draw, body, font_path, (content_x, y), content_width, 220, 34, 20, "#243B53"
    )
    y += 28

    disclaimer_top = 930
    disclaimer_height = 70
    bottom_padding = CANVAS_SIZE[1] - (disclaimer_top + disclaimer_height)
    if bottom_padding < 48:
        raise ValueError("Disclaimer area does not have enough bottom padding.")

    offer_gap = 28
    offer_top = y
    available_offer_height = disclaimer_top - offer_gap - offer_top
    if available_offer_height <= 56:
        raise ValueError(
            "Headline and body leave no room for the offer box before the disclaimer."
        )
    offer_font, offer_lines, offer_line_height = _fit_text(
        offer,
        font_path,
        content_width - 64,
        available_offer_height - 56,
        38,
        18,
    )
    offer_height = len(offer_lines) * offer_line_height + 56
    offer_bottom = offer_top + offer_height
    if offer_bottom + offer_gap > disclaimer_top:
        raise ValueError("Offer text cannot fit before the disclaimer area.")

    draw.rounded_rectangle(
        (content_x, offer_top, content_x + content_width, offer_bottom),
        radius=24,
        fill="#D9A441",
    )
    offer_y = offer_top + 28
    for line in offer_lines:
        draw.text((content_x + 32, offer_y), line, font=offer_font, fill="#102A43")
        offer_y += offer_line_height

    _draw_text_block(
        draw,
        disclaimer,
        font_path,
        (content_x, disclaimer_top),
        content_width,
        70,
        22,
        12,
        "#52606D",
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{creative_id}.png"
    image.save(output_path, format="PNG")
    return output_path


def render_placeholder(output_path: Path) -> Path:
    """Save a blank 1080x1080 RGB canvas and return its path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", CANVAS_SIZE, "white").save(output_path)
    return output_path
