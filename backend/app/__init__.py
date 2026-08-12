import os
from flask import Flask, jsonify
from flask_cors import CORS
from app.config import config_by_name
from app.extensions import db
from app.routes import register_routes


def create_app(env=None):
    env = env or os.environ.get("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name[env])

    os.makedirs(os.path.join(app.root_path, "..", "instance"), exist_ok=True)

    CORS(app)  # allow the React frontend (different origin) to call this API
    db.init_app(app)
    register_routes(app)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "task-management-api"}), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    with app.app_context():
        db.create_all()

    return app
