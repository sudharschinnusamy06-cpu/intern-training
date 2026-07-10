from app.models import Task


def test_task_creation_with_valid_data():
    task = Task(title="Learn pytest", description="Write unit tests today")

    assert task.title == "Learn pytest"
    assert not task.completed


def test_task_missing_title_defaults_to_none():
    task = Task(description="Missing the title field")

    assert task.title is None
