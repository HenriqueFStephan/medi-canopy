"""Courses showcase API."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

COURSE_001_ID = "course-001"
COURSE_001_TITLE = (
    "Produção de Flores de Cannabis de Grau Medicinal: O Modelo Canadense"
)
COURSE_001_MODULES = [
    "Parte I – Introdução à Cannabis Sativa: Uma Perspectiva Histórica",
    "Parte II – Do Cultivo ao Consumidor: Como Funciona a Regulação Canadense",
    "Parte III – Planejamento Produtivo e Operacional de Cannabis Medicinal",
    "Parte IV – Caracterização e Gestão do Material Genético de Cannabis Medicinal",
    "Parte V – Manejo Integrado de Pragas (MIP)",
    "Parte VI – A Ciência por Trás da Colheita",
    "Parte VII – Pós-Colheita e Preservação do Produto",
    "Parte VIII – Rastreabilidade e Controle de Qualidade",
    "Parte IX – Gestão e Documentação",
    "Parte X – Agricultura de Precisão e Tendências Tecnológicas",
]


def test_list_courses_includes_updated_course_001():
    response = client.get("/api/v1/courses")
    assert response.status_code == 200
    data = response.json()
    course = next(item for item in data if item["id"] == COURSE_001_ID)
    assert course["title"] == COURSE_001_TITLE
    assert course["level"] == "profissional"
    assert course["description"] == (
        "Princípios, práticas e padrões para uma produção de alta qualidade"
    )
    assert [module["title"] for module in course["modules"]] == COURSE_001_MODULES


def test_get_course_001_by_id():
    response = client.get(f"/api/v1/courses/{COURSE_001_ID}")
    assert response.status_code == 200
    course = response.json()
    assert course["title"] == COURSE_001_TITLE
    assert len(course["modules"]) == 10
