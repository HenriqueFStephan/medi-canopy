"""Courses API — placeholder architecture for future LMS integration."""

from fastapi import APIRouter, HTTPException, Query

from app.core.locale import localize_item, localize_list, normalize_lang
from app.models.schemas import Course
from app.repositories.json_store import courses_store

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[Course])
def list_courses(lang: str | None = Query(default=None)) -> list[Course]:
    locale = normalize_lang(lang)
    return [Course.model_validate(i) for i in localize_list(courses_store.read_all(), locale)]


@router.get("/{course_id}", response_model=Course)
def get_course(course_id: str, lang: str | None = Query(default=None)) -> Course:
    locale = normalize_lang(lang)
    for item in courses_store.read_all():
        if item["id"] == course_id:
            return Course.model_validate(localize_item(item, locale))
    raise HTTPException(status_code=404, detail="Course not found")
