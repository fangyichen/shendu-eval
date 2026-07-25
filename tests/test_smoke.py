"""Phase 0 smoke tests: the package imports and the task constructs cleanly."""

from inspect_ai import Task

from shendu.tasks import smoke


def test_smoke_task_constructs():
    task = smoke()
    assert isinstance(task, Task)
    assert task.dataset is not None
    assert len(task.dataset) == 1
