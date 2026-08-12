from datetime import datetime, timezone
from app.extensions import db


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    author = db.Column(db.String(100), default="Anonymous")
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "author": self.author,
            "body": self.body,
            "created_at": self.created_at.isoformat(),
        }
