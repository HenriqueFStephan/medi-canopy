"""UTF-8 / Windows-1252 mojibake repair for Portuguese copy."""

from app.core.text_encoding import repair_mojibake, repair_mojibake_text


def _garbled(text: str) -> str:
    """Simulate UTF-8 bytes being decoded as Windows-1252."""
    return text.encode("utf-8").decode("cp1252")


def test_repairs_portuguese_title_and_excerpt():
    title = "Regulamentação no Brasil: o que mudou para cultivadores em 2026"
    excerpt = "Panorama político e regulatório com foco prático para quem opera."

    assert repair_mojibake_text(_garbled(title)) == title
    assert repair_mojibake_text(_garbled(excerpt)) == excerpt


def test_repairs_em_dash_mojibake():
    original = "sem cair em hype — guia rápido"
    assert repair_mojibake_text(_garbled(original)) == original


def test_leaves_correct_portuguese_unchanged():
    original = "Regulamentação no Brasil: panorama político e prático."
    assert repair_mojibake_text(original) == original


def test_leaves_ascii_and_empty_unchanged():
    assert repair_mojibake_text("Instagram") == "Instagram"
    assert repair_mojibake_text("") == ""


def test_repairs_nested_payloads():
    payload = {
        "title": _garbled("Benefícios medicinais"),
        "tags": ["brazil"],
        "nested": [{"excerpt": _garbled("orientações da ANVISA")}],
    }
    assert repair_mojibake(payload) == {
        "title": "Benefícios medicinais",
        "tags": ["brazil"],
        "nested": [{"excerpt": "orientações da ANVISA"}],
    }
