from app.models.schemas import ServiceOffering


def test_strips_leading_index_from_service_title():
    item = ServiceOffering.model_validate(
        {
            "id": "svc-viability",
            "title": "01 — Viabilidade & Investimentos",
            "description": "CAPEX • OPEX",
            "icon": "chart",
        }
    )
    assert item.title == "Viabilidade & Investimentos"


def test_leaves_unnumbered_title_unchanged():
    item = ServiceOffering.model_validate(
        {
            "id": "svc-viability",
            "title": "Viabilidade & Investimentos",
            "description": "CAPEX • OPEX",
            "icon": "chart",
        }
    )
    assert item.title == "Viabilidade & Investimentos"
