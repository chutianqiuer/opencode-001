import io
import random
import string
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
from app.config import settings


def generate_captcha() -> Tuple[str, bytes]:
    chars = string.ascii_uppercase + string.digits
    chars = chars.replace("O", "").replace("0", "").replace("I", "").replace("1", "")
    code = "".join(random.choices(chars, k=4))
    width, height = 120, 40
    image = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except Exception:
        font = ImageFont.load_default()
    for i, char in enumerate(code):
        x = 20 + i * 25
        y = random.randint(5, 10)
        color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        draw.text((x, y), char, font=font, fill=color)
    for _ in range(random.randint(3, 6)):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        color = (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))
        draw.line([(x1, y1), (x2, y2)], fill=color, width=1)
    for _ in range(random.randint(50, 100)):
        x = random.randint(0, width)
        y = random.randint(0, height)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.point((x, y), fill=color)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()
    return code, image_bytes
