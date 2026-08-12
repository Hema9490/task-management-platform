from flask import Blueprint, request, jsonify
from app.repository import task_repo, project_repo
from app.models.task import VALID_STATUSES, VALID_PRIORITIES

bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


@bp.get("")
def list_tasks():
    status = request.args.get("status")
    project_id = request.args.get("project_id", type=int)

    if project_id:
        tasks = task_repo.get_by_project(project_id)
    elif status:
        tasks = task_repo.get_by_status(status)
    else:
        tasks = task_repo.get_all()
    return jsonify([t.to_dict() for t in tasks]), 200


@bp.post("")
def create_task():
    data = request.get_json(silent=True) or {}
    project_id = data.get("project_id")
    title = data.get("title")

    if not project_id or not title:
        return jsonify({"error": "'project_id' and 'title' are required"}), 400
    if not project_repo.get(project_id):
        return jsonify({"error": "Project not found"}), 404

    status = data.get("status", "todo")
    priority = data.get("priority", "medium")
    if status not in VALID_STATUSES:
        return jsonify({"error": f"status must be one of {VALID_STATUSES}"}), 400
    if priority not in VALID_PRIORITIES:
        return jsonify({"error": f"priority must be one of {VALID_PRIORITIES}"}), 400

    task = task_repo.create(
        project_id=project_id,
        title=title,
        description=data.get("description", ""),
        status=status,
        priority=priority,
        assignee=data.get("assignee", ""),
    )
    return jsonify(task.to_dict()), 201


@bp.get("/<int:task_id>")
def get_task(task_id):
    task = task_repo.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_dict(include_comments=True)), 200


@bp.put("/<int:task_id>")
def update_task(task_id):
    task = task_repo.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True) or {}
    if "status" in data and data["status"] not in VALID_STATUSES:
        return jsonify({"error": f"status must be one of {VALID_STATUSES}"}), 400
    if "priority" in data and data["priority"] not in VALID_PRIORITIES:
        return jsonify({"error": f"priority must be one of {VALID_PRIORITIES}"}), 400

    task = task_repo.update(
        task,
        title=data.get("title"),
        description=data.get("description"),
        status=data.get("status"),
        priority=data.get("priority"),
        assignee=data.get("assignee"),
    )
    return jsonify(task.to_dict()), 200


@bp.delete("/<int:task_id>")
def delete_task(task_id):
    task = task_repo.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task_repo.delete(task)
    return jsonify({"message": "Task deleted"}), 200
