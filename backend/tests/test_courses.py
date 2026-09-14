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


COURSE_002_ID = "course-002"
COURSE_002_TITLE = "Genética, Biologia Vegetal e Melhoramento Aplicado da Cannabis"
COURSE_002_SUBTITLE = "Transformando conhecimento genético em potencial agronômico"
COURSE_002_LEVEL = "avançado"

COURSE_002_MODULES = [
    "Módulo 1 — Introdução à Genética para o Melhoramento de Plantas",
    "Módulo 2 — DNA, RNA e a Base Molecular da Vida no Melhoramento de Plantas",
    "Módulo 3 — Biologia Celular e Divisão Celular no Melhoramento Genético da Cannabis",
    "Módulo 4 — Genética de Populações e Diversidade Genética no Melhoramento da Cannabis",
    "Módulo 5 — Reprodução das Plantas e Ciclos de Vida (para o Melhoramento da Cannabis)",
    "Módulo 6 — Hormônios Vegetais e Regulação Gênica no Melhoramento da Cannabis",
    "Módulo 7 — Genética da Cannabis e Quimiotipos",
    "Módulo 8 — Técnicas de Melhoramento da Cannabis (Estrutura Conceitual)",
    "Módulo 9 — Genética Molecular Avançada no Melhoramento da Cannabis – Genômica e Melhoramento Assistido por Marcadores",
    "Módulo 10 — Diversidade Genética, Conservação e Ética no Melhoramento da Cannabis",
]


def test_list_courses_includes_updated_course_002():
    response = client.get("/api/v1/courses")
    assert response.status_code == 200
    data = response.json()
    course = next(item for item in data if item["id"] == COURSE_002_ID)
    assert course["title"] == COURSE_002_TITLE
    assert course["description"] == COURSE_002_SUBTITLE
    assert course["level"] == COURSE_002_LEVEL
    assert [module["title"] for module in course["modules"]] == COURSE_002_MODULES


def test_get_course_002_by_id():
    response = client.get(f"/api/v1/courses/{COURSE_002_ID}")
    assert response.status_code == 200
    course = response.json()
    assert course["title"] == COURSE_002_TITLE
    assert len(course["modules"]) == 10
