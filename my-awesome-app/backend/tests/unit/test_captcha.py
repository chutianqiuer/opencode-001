import pytest
from app.utils.captcha import generate_captcha


def test_generate_captcha_returns_tuple():
    result = generate_captcha()
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_generate_captcha_code_format():
    code, image_bytes = generate_captcha()
    assert isinstance(code, str)
    assert len(code) == 4
    assert code.isalnum()
    assert "O" not in code
    assert "0" not in code
    assert "I" not in code
    assert "1" not in code


def test_generate_captcha_image_bytes():
    code, image_bytes = generate_captcha()
    assert isinstance(image_bytes, bytes)
    assert len(image_bytes) > 0


def test_generate_multiple_captchas_unique():
    codes = set()
    for _ in range(10):
        code, _ = generate_captcha()
        codes.add(code)
    assert len(codes) > 1


def test_captcha_image_is_png():
    import io
    from PIL import Image

    code, image_bytes = generate_captcha()
    image_stream = io.BytesIO(image_bytes)
    image = Image.open(image_stream)
    assert image.format == "PNG"
    assert image.size == (120, 40)
