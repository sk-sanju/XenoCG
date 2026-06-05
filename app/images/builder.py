import os
import random
import io
from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from ..config import BRAND_LOGO_PATH, BRAND_PRIMARY_COLOR, BRAND_ACCENT_COLOR

# Constants
IMAGE_SIZE = (1080, 1080)  # Instagram square
FONT_PATH = None  # Will fallback to a default PIL font if not provided
FONT_SIZE = 48

def _load_logo() -> Image.Image:
    """Load the branding logo if it exists, otherwise create a simple placeholder."""
    logo_path = Path(BRAND_LOGO_PATH)
    if logo_path.is_file():
        return Image.open(logo_path).convert("RGBA")
    # Create a placeholder logo: dark circle with white text "X".
    logo = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(logo)
    draw.ellipse([(0, 0), (200, 200)], fill=BRAND_ACCENT_COLOR)
    # Use default font for placeholder "X"
    font = ImageFont.load_default()
    w, h = draw.textsize("X", font=font)
    draw.text(((200 - w) / 2, (200 - h) / 2), "X", fill="white", font=font)
    return logo

def _apply_branding(base_image: Image.Image, title: str) -> Image.Image:
    """Overlay the branding logo and title text onto the base image.
    - Logo placed at bottom‑right with margin.
    - Title centered near the top.
    """
    img = base_image.convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Add title text
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE) if FONT_PATH else ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()
    text = title
    text_w, text_h = draw.textsize(text, font=font)
    text_position = ((IMAGE_SIZE[0] - text_w) // 2, 40)
    # Semi‑transparent rectangle behind text for readability
    padding = 10
    rect_xy = [
        (text_position[0] - padding, text_position[1] - padding),
        (text_position[0] + text_w + padding, text_position[1] + text_h + padding)
    ]
    draw.rectangle(rect_xy, fill=(0, 0, 0, 120))
    draw.text(text_position, text, font=font, fill="white")

    # Add logo
    logo = _load_logo().resize((150, 150), Image.ANTIALIAS)
    logo_margin = 30
    logo_position = (IMAGE_SIZE[0] - logo.width - logo_margin, IMAGE_SIZE[1] - logo.height - logo_margin)
    img.paste(logo, logo_position, logo)
    return img

def generate_branded_image(title: str, output_path: Path) -> Path:
    """Create a branded image for a post.
    If a stock image URL is provided later, this function can be extended to use it.
    For now it creates a solid background with the brand colors.
    """
    # Simple solid background using primary brand color
    bg_color = BRAND_PRIMARY_COLOR
    # Convert hex to RGB tuple
    bg_rgb = tuple(int(bg_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    base = Image.new("RGB", IMAGE_SIZE, bg_rgb)
    branded = _apply_branding(base, title)
    branded.save(output_path, format="JPEG", quality=90)
    return output_path
