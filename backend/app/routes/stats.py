from collections import defaultdict
from datetime import datetime, timezone
from flask import Blueprint, jsonify
from app.models import Task, Project

bp = Blueprint("stats", __name__, url_prefix="/api/stats")


@bp.get("/overview")
def overview():
    """High-level KPI numbers for the dashboard header."""
    tasks = Task.query.all()
    total = len(tasks)
    done = sum(1 for t in tasks if t.status == "done")
    in_progress = sum(1 for t in tasks if t.status == "in_progress")
    todo = sum(1 for t in tasks if t.status == "todo")

    closed = [t for t in tasks if t.closed_at is not None]
    if closed:
        avg_seconds = sum(
            (t.closed_at - t.created_at).total_seconds() for t in closed
        ) / len(closed)
        avg_close_time_hours = round(avg_seconds / 3600, 1)
    else:
        avg_close_time_hours = None

    return jsonify({
        "total_projects": Project.query.count(),
        "total_tasks": total,
        "done": done,
        "in_progress": in_progress,
        "todo": todo,
        "completion_rate_pct": round((done / total) * 100, 1) if total else 0,
        "avg_close_time_hours": avg_close_time_hours,
    }), 200


@bp.get("/tasks-per-week")
def tasks_per_week():
    """Tasks created, grouped by ISO week - powers a trend chart."""
    tasks = Task.query.all()
    buckets = defaultdict(int)
    for t in tasks:
        year, week, _ = t.created_at.isocalendar()
        key = f"{year}-W{week:02d}"
        buckets[key] += 1
    series = [{"week": k, "count": v} for k, v in sorted(buckets.items())]
    return jsonify(series), 200


@bp.get("/by-priority")
def by_priority():
    tasks = Task.query.all()
    buckets = defaultdict(int)
    for t in tasks:
        buckets[t.priority] += 1
    return jsonify(buckets), 200
