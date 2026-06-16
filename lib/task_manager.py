from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


class TaskManager:
    """Manage tasks for users and persist them to a JSON file.

    Tasks are stored in a dict mapping username -> list of task dicts.
    Each task dict has: id (int), description (str), completed (bool), created_at (ISO str)
    """

    def __init__(self, storage: str | Path | None = None):
        self.storage = Path(storage) if storage else Path("tasks.json")
        self._data: Dict[str, List[Dict]] = {}
        self._load()

    def _load(self) -> None:
        if self.storage.exists():
            try:
                with self.storage.open("r", encoding="utf-8") as fh:
                    self._data = json.load(fh)
            except Exception:
                self._data = {}
        else:
            self._data = {}

    def _save(self) -> None:
        self.storage.parent.mkdir(parents=True, exist_ok=True)
        with self.storage.open("w", encoding="utf-8") as fh:
            json.dump(self._data, fh, indent=2)

    def add_task(self, user: str, description: str) -> Dict:
        if not isinstance(user, str) or not user:
            raise ValueError("user must be a non-empty string")
        if not isinstance(description, str) or not description:
            raise ValueError("description must be a non-empty string")

        tasks = self._data.setdefault(user, [])
        next_id = 1 + max((t.get("id", 0) for t in tasks), default=0)
        task = {
            "id": next_id,
            "description": description,
            "completed": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        tasks.append(task)
        self._save()
        return task

    def complete_task(self, user: str, task_id: int) -> Dict:
        if not isinstance(task_id, int):
            raise ValueError("task_id must be an integer")
        tasks = self._data.get(user, [])
        for t in tasks:
            if t.get("id") == task_id:
                t["completed"] = True
                self._save()
                return t
        raise KeyError(f"Task id {task_id} not found for user {user}")

    def list_tasks(self, user: str) -> List[Dict]:
        return list(self._data.get(user, []))
