#!/usr/bin/env python3
"""Simple CLI for managing tasks using TaskManager."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from lib.task_manager import TaskManager


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taskcli")
    sub = parser.add_subparsers(dest="command")

    add = sub.add_parser("add-task", help="Add a task for a user")
    add.add_argument("user", help="Username")
    add.add_argument("description", help="Task description")

    comp = sub.add_parser("complete-task", help="Mark a task as complete")
    comp.add_argument("user", help="Username")
    comp.add_argument("task_id", type=int, help="Task ID to complete")

    listp = sub.add_parser("list-tasks", help="List tasks for a user")
    listp.add_argument("user", help="Username")

    parser.add_argument("--storage", help="Path to tasks storage file", default="tasks.json")
    return parser


def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    mgr = TaskManager(storage=Path(args.storage))

    if args.command == "add-task":
        task = mgr.add_task(args.user, args.description)
        print(f"Added task {task['id']} for {args.user}: {task['description']}")
    elif args.command == "complete-task":
        try:
            task = mgr.complete_task(args.user, args.task_id)
            print(f"Completed task {task['id']} for {args.user}")
        except KeyError as e:
            print(e)
            return 1
    elif args.command == "list-tasks":
        tasks = mgr.list_tasks(args.user)
        if not tasks:
            print("No tasks found")
        for t in tasks:
            status = "✓" if t.get("completed") else " "
            print(f"[{status}] {t['id']}: {t['description']}")
    else:
        parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
