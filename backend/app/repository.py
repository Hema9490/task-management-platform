"""
Repository pattern layer.

Routes never talk to db.session or SQLAlchemy models directly - they go
through a Repository. This keeps query logic in one place, makes the
route handlers thin, and makes the data layer swappable/unit-testable.
"""
from datetime import datetime, timezone
from app.extensions import db
from app.models import Project, Task, Comment


class BaseRepository:
    model = None

    def get(self, id):
        return self.model.query.get(id)

    def get_all(self):
        return self.model.query.all()

    def delete(self, instance):
        db.session.delete(instance)
        db.session.commit()

    def _save(self, instance):
        db.session.add(instance)
        db.session.commit()
        return instance


class ProjectRepository(BaseRepository):
    model = Project

    def create(self, name, description="", status="active"):
        project = Project(name=name, description=description, status=status)
        return self._save(project)

    def update(self, project, **fields):
        for key, value in fields.items():
            if value is not None and hasattr(project, key):
                setattr(project, key, value)
        return self._save(project)


class TaskRepository(BaseRepository):
    model = Task

    def create(self, project_id, title, **fields):
        task = Task(project_id=project_id, title=title, **fields)
        return self._save(task)

    def update(self, task, **fields):
        for key, value in fields.items():
            if value is None or not hasattr(task, key):
                continue
            setattr(task, key, value)
            if key == "status":
                task.closed_at = datetime.now(timezone.utc) if value == "done" else None
        return self._save(task)

    def get_by_project(self, project_id):
        return Task.query.filter_by(project_id=project_id).all()

    def get_by_status(self, status):
        return Task.query.filter_by(status=status).all()


class CommentRepository(BaseRepository):
    model = Comment

    def create(self, task_id, body, author="Anonymous"):
        comment = Comment(task_id=task_id, body=body, author=author)
        return self._save(comment)

    def get_by_task(self, task_id):
        return Comment.query.filter_by(task_id=task_id).all()


project_repo = ProjectRepository()
task_repo = TaskRepository()
comment_repo = CommentRepository()
