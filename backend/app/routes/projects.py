from flask import Blueprint, request, jsonify
from app.repository import project_repo

bp = Blueprint("projects", __name__, url_prefix="/api/projects")


@bp.get("")
def list_projects():
    projects = project_repo.get_all()
    return jsonify([p.to_dict() for p in projects]), 200


@bp.post("")
def create_project():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "'name' is required"}), 400
    project = project_repo.create(
        name=name,
        description=data.get("description", ""),
        status=data.get("status", "active"),
    )
    return jsonify(project.to_dict()), 201


@bp.get("/<int:project_id>")
def get_project(project_id):
    project = project_repo.get(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project.to_dict(include_tasks=True)), 200


@bp.put("/<int:project_id>")
def update_project(project_id):
    project = project_repo.get(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    data = request.get_json(silent=True) or {}
    project = project_repo.update(
        project,
        name=data.get("name"),
        description=data.get("description"),
        status=data.get("status"),
    )
    return jsonify(project.to_dict()), 200


@bp.delete("/<int:project_id>")
def delete_project(project_id):
    project = project_repo.get(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    project_repo.delete(project)
    return jsonify({"message": "Project deleted"}), 200
