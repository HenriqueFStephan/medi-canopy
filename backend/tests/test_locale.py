"""Public API localisation (pt-BR / en)."""

from app.core.locale import localize_item, normalize_lang


def test_normalize_lang_defaults_to_pt():
    assert normalize_lang(None) == "pt-BR"
    assert normalize_lang("pt") == "pt-BR"
    assert normalize_lang("pt-BR") == "pt-BR"
    assert normalize_lang("en") == "en"
    assert normalize_lang("en-US") == "en"


def test_localize_item_uses_title_pt_for_portuguese():
    item = {
        "id": "blog-1",
        "title": "English original title",
        "title_pt": "Título em português",
        "excerpt": "Resumo em português",
        "i18n": {"en": {"excerpt": "English excerpt"}},
    }
    pt = localize_item(item, "pt-BR")
    en = localize_item(item, "en")
    assert pt["title"] == "Título em português"
    assert en["title"] == "English original title"
    assert en["excerpt"] == "English excerpt"
    assert "i18n" not in pt
    assert "i18n" not in en


def test_list_blog_titles_switch_with_lang():
    from fastapi.testclient import TestClient

    from app.main import app

    api = TestClient(app)
    pt = api.get("/api/v1/blog", params={"lang": "pt-BR"})
    en = api.get("/api/v1/blog", params={"lang": "en"})
    assert pt.status_code == 200
    assert en.status_code == 200
    pt_titles = [row["title"] for row in pt.json()]
    en_titles = [row["title"] for row in en.json()]
    assert pt_titles
    assert en_titles
    assert pt_titles != en_titles
    assert any("Caracterização fenotípica" in title for title in pt_titles)
    assert any("Phenotypic and genetic characterization" in title for title in en_titles)


def test_list_services_english():
    from fastapi.testclient import TestClient

    from app.main import app

    api = TestClient(app)
    response = api.get("/api/v1/services", params={"lang": "en"})
    assert response.status_code == 200
    titles = [row["title"] for row in response.json()]
    assert titles[0] == "Viability & Investments"


def test_contact_message_follows_lang():
    from fastapi.testclient import TestClient

    from app.main import app

    api = TestClient(app)
    payload = {
        "name": "Ana Silva",
        "email": "ana@example.com",
        "subject": "Hello there",
        "message": "This is a long enough contact message.",
    }
    pt = api.post("/api/v1/contact", json=payload)
    en = api.post("/api/v1/contact", params={"lang": "en"}, json=payload)
    assert "Retornaremos" in pt.json()["message"]
    assert "get back to you" in en.json()["message"]
