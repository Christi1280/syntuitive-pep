from flask import Blueprint, abort, redirect, render_template, request, session, url_for

from app.data.curriculum import (
    DEFAULT_GRADE,
    get_subjects,
    is_supported_grade,
)

student_bp = Blueprint("student", __name__)


@student_bp.get("/dashboard")
def dashboard():
    grade = session.get("grade", DEFAULT_GRADE)
    return render_template(
        "dashboard.html",
        title="Dashboard",
        active_page="Dashboard",
        grade=grade,
        subjects=get_subjects(grade),
    )


@student_bp.post("/grade")
def set_grade():
    try:
        grade = int(request.form.get("grade", ""))
    except ValueError:
        abort(400)
    if not is_supported_grade(grade):
        abort(400)

    session["grade"] = grade
    return redirect(url_for("student.dashboard"))


@student_bp.get("/progress")
def progress():
    grade = session.get("grade", DEFAULT_GRADE)
    return render_template(
        "progress.html",
        title="My Progress",
        active_page="My Progress",
        grade=grade,
        subjects=get_subjects(grade),
    )


@student_bp.get("/achievements")
def achievements():
    return render_template("achievements.html", title="Achievements", active_page="Achievements")


@student_bp.get("/settings")
def settings():
    return render_template("settings.html", title="Settings", active_page="Settings")
