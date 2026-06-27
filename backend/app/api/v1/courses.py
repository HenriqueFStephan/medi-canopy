"""Courses API — placeholder architecture for future LMS integration."""

from fastapi import APIRouter, HTTPException

from app.models.schemas import Course
from app.repositories.json_store import courses_store

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[Course])
def list_courses() -> list[Course]:
    return [Course.model_validate(i) for i in courses_store.read_all()]


@router.get("/{course_id}", response_model=Course)
def get_course(course_id: str) -> Course:
    for item in courses_store.read_all():
        if item["id"] == course_id:
            return Course.model_validate(item)
    raise HTTPException(status_code=404, detail="Course not found")
