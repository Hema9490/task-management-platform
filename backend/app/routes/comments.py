from flask import Blueprint, request, jsonify
from app.repository import comment_repo, task_repo

bp = Blueprint("comments", __name__, url_prefix="/api/tasks/<int:task_id>/comments")


@bp.get("")
def list_comments(task_id):
    if not task_repo.get(task_id):
        return jsonify({"error": "Task not found"}), 404
    comments = comment_repo.get_by_task(task_id)
    return jsonify([c.to_dict() for c in comments]), 200


@bp.post("")
def create_comment(task_id):
    if not task_repo.get(task_id):
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json(silent=True) or {}
    body = data.get("body")
    if not body:
        return jsonify({"error": "'body' is required"}), 400
    comment = comment_repo.create(
        task_id=task_id, body=body, author=data.get("author", "Anonymous")
    )
    return jsonify(comment.to_dict()), 201
