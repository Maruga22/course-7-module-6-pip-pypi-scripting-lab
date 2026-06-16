import os
import tempfile
from pathlib import Path

import pytest

from lib.task_manager import TaskManager


@pytest.fixture
def tmp_storage(tmp_path):
    return tmp_path / "tasks.json"


def test_add_and_list_tasks(tmp_storage):
    mgr = TaskManager(storage=tmp_storage)
    task = mgr.add_task("alice", "Write tests")
    assert task["id"] == 1
    assert task["description"] == "Write tests"
    tasks = mgr.list_tasks("alice")
    assert len(tasks) == 1


def test_complete_task(tmp_storage):
    mgr = TaskManager(storage=tmp_storage)
    mgr.add_task("bob", "Implement feature")
    completed = mgr.complete_task("bob", 1)
    assert completed["completed"] is True


def test_complete_missing_task_raises(tmp_storage):
    mgr = TaskManager(storage=tmp_storage)
    with pytest.raises(KeyError):
        mgr.complete_task("carol", 42)


def test_persistence(tmp_storage):
    mgr = TaskManager(storage=tmp_storage)
    mgr.add_task("dave", "Persist me")
    # create a new manager with same storage to ensure data persisted
    mgr2 = TaskManager(storage=tmp_storage)
    tasks = mgr2.list_tasks("dave")
    assert tasks and tasks[0]["description"] == "Persist me"
