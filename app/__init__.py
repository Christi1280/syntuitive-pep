import os

from flask import Flask, session

from app.data.curriculum import DEFAULT_GRADE, SUPPORTED_GRADES, is_supported_grade


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me"))
    if test_config:
        app.config.update(test_config)

    @app.before_request
    def ensure_selected_grade():
        grade = session.get("grade", DEFAULT_GRADE)
        if not is_supported_grade(grade):
            session["grade"] = DEFAULT_GRADE

    @app.context_processor
    def inject_selected_grade():
        return {
            "current_grade": session.get("grade", DEFAULT_GRADE),
            "supported_grades": SUPPORTED_GRADES,
        }

    from app.routes.admin import admin_bp
    from app.routes.learning import learning_bp
    from app.routes.main import main_bp
    from app.routes.practice import practice_bp
    from app.routes.student import student_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(practice_bp)
    app.register_blueprint(admin_bp)
    return app
