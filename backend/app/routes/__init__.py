from app.routes import projects, tasks, comments, stats


def register_routes(app):
    app.register_blueprint(projects.bp)
    app.register_blueprint(tasks.bp)
    app.register_blueprint(comments.bp)
    app.register_blueprint(stats.bp)
