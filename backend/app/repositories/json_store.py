"""
JSON-file backed data store for demo phase.

Replace with SQLAlchemy repository when migrating to PostgreSQL.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generic, TypeVar

from app.core.config import BACKEND_ROOT

T = TypeVar("T")

SEED_DIR = BACKEND_ROOT / "data" / "seed"
DATA_DIR = BACKEND_ROOT / "data"
REVIEW_FILE = DATA_DIR / "review_queue.json"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class JsonStore:
    """Simple JSON persistence for list-based collections."""

    def __init__(self, path: Path, seed_path: Path | None = None):
        self.path = path
        self.seed_path = seed_path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self._should_seed() and self.seed_path is not None:
            self.path.write_text(self.seed_path.read_text(encoding="utf-8"), encoding="utf-8")
        elif not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def _should_seed(self) -> bool:
        """Copy seed when the store is missing or still an empty list."""
        if not self.seed_path or not self.seed_path.exists():
            return False
        if not self.path.exists():
            return True
        try:
            return json.loads(self.path.read_text(encoding="utf-8")) == []
        except (json.JSONDecodeError, OSError):
            return True

    def load_seed(self) -> None:
        """Replace this store with its seed file (demo reset)."""
        if not self.seed_path or not self.seed_path.exists():
            raise FileNotFoundError(f"No seed file for {self.path.name}")
        self.path.write_text(self.seed_path.read_text(encoding="utf-8"), encoding="utf-8")

    def read_all(self) -> list[dict[str, Any]]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def write_all(self, items: list[dict[str, Any]]) -> None:
        self.path.write_text(json.dumps(items, indent=2, default=str), encoding="utf-8")

    def append(self, item: dict[str, Any]) -> dict[str, Any]:
        items = self.read_all()
        items.append(item)
        self.write_all(items)
        return item


# Collection stores
news_store = JsonStore(DATA_DIR / "news.json", SEED_DIR / "news.json")
blog_store = JsonStore(DATA_DIR / "blog.json", SEED_DIR / "blog.json")
courses_store = JsonStore(DATA_DIR / "courses.json", SEED_DIR / "courses.json")
services_store = JsonStore(DATA_DIR / "services.json", SEED_DIR / "services.json")
contact_store = JsonStore(DATA_DIR / "contact_messages.json")


def get_review_queue() -> list[dict[str, Any]]:
    if not REVIEW_FILE.exists():
        REVIEW_FILE.write_text("[]", encoding="utf-8")
    return json.loads(REVIEW_FILE.read_text(encoding="utf-8"))


def save_review_queue(items: list[dict[str, Any]]) -> None:
    REVIEW_FILE.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_FILE.write_text(json.dumps(items, indent=2, default=str), encoding="utf-8")


def new_id() -> str:
    return str(uuid.uuid4())
