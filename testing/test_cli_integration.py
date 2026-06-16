import os
import subprocess
import sys
from pathlib import Path


def cli_script_path():
    return Path(__file__).parents[1] / "bin" / "taskcli.py"


def run_cli(args, storage_path):
    # `--storage` is a global option; pass it before the subcommand
    cmd = [sys.executable, str(cli_script_path()), "--storage", str(storage_path)] + args
    env = dict(os.environ)
    # Ensure the repository root is on PYTHONPATH so `lib` imports resolve
    env["PYTHONPATH"] = str(Path(__file__).parents[1])
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return result


def test_add_and_list_tasks_cli(tmp_path):
    storage = tmp_path / "tasks.json"
    add = run_cli(["add-task", "alice", "Do stuff"], storage)
    assert add.returncode == 0
    assert "Added task 1 for alice" in add.stdout

    list_res = run_cli(["list-tasks", "alice"], storage)
    assert list_res.returncode == 0
    assert "1: Do stuff" in list_res.stdout


def test_complete_task_cli(tmp_path):
    storage = tmp_path / "tasks.json"
    run_cli(["add-task", "bob", "Finish feature"], storage)
    comp = run_cli(["complete-task", "bob", "1"], storage)
    assert comp.returncode == 0
    assert "Completed task 1 for bob" in comp.stdout

    list_res = run_cli(["list-tasks", "bob"], storage)
    assert "✓" in list_res.stdout or "[" in list_res.stdout
