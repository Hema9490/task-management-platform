from datetime import datetime, timezone
from app.extensions import db

VALID_STATUSES = ("todo", "in_progress", "done")
VALID_PRIORITIES = ("low", "medium", "high")


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, default="")
    status = db.Column(db.String(20), default="todo")
    priority = db.Column(db.String(10), default="medium")
    assignee = db.Column(db.String(100), default="")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    closed_at = db.Column(db.DateTime, nullable=True)

    comments = db.relationship(
        "Comment", backref="task", cascade="all, delete-orphan", lazy=True
    )

    def to_dict(self, include_comments=False):
        data = {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "assignee": self.assignee,
            "created_at": self.created_at.isoformat(),
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
        }
        if include_comments:
            data["comments"] = [c.to_dict() for c in self.comments]
        return data
