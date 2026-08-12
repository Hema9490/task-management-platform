from datetime import datetime, timezone
from app.extensions import db


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    status = db.Column(db.String(20), default="active")  # active | archived
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    tasks = db.relationship(
        "Task", backref="project", cascade="all, delete-orphan", lazy=True
    )

    def to_dict(self, include_tasks=False):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "task_count": len(self.tasks),
        }
        if include_tasks:
            data["tasks"] = [t.to_dict() for t in self.tasks]
        return data
