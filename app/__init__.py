import os
from secrets import token_urlsafe

from flask import Flask, session

from app.data.curriculum import DEFAULT_GRADE, SUPPORTED_GRADES, is_supported_grade


def create_app(test_config=None, *, local=False):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY"),
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=not local,
    )
    if test_config is not None:
        app.config.update(test_config)
    if not app.secret_key:
        if not local:
            raise RuntimeError("Set FLASK_SECRET_KEY before starting the application.")
        app.secret_key = token_urlsafe(32)

    @app.before_request
    def ensure_selected_grade():
        grade = session.get("grade", DEFAULT_GRADE)
        if not is_supported_grade(grade):
            session["grade"] = DEFAULT_GRADE

    @app.context_processor
    def inject_grade_form():
        if "grade_csrf_token" not in session:
            session["grade_csrf_token"] = token_urlsafe(32)
        return {
            "current_grade": session.get("grade", DEFAULT_GRADE),
            "supported_grades": SUPPORTED_GRADES,
            "grade_csrf_token": session["grade_csrf_token"],
        }

    from app.routes.main import main_bp
    from app.routes.practice import practice_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(practice_bp)
    return app
