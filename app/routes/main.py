from secrets import compare_digest

from flask import Blueprint, abort, redirect, render_template, request, session, url_for

from app.data.curriculum import is_supported_grade

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return render_template(
        "index.html",
        title="PEP practice made simple",
        active_page="Home",
    )


@main_bp.post("/grade")
def set_grade():
    expected_token = session.get("grade_csrf_token")
    submitted_token = request.form.get("grade_csrf_token", "")
    if not expected_token or not compare_digest(
        expected_token.encode(), submitted_token.encode()
    ):
        abort(400, "Invalid grade form token. Reload the page and try again.")

    try:
        grade = int(request.form.get("grade", ""))
    except ValueError:
        abort(400)
    if not is_supported_grade(grade):
        abort(400)

    session["grade"] = grade
    destination = request.form.get("return_to", "").partition("#")[0]
    path = destination.partition("?")[0]
    home = url_for("main.index")
    allowed_paths = {
        home,
        url_for("practice.flashcards"),
        url_for("practice.practice"),
        url_for("practice.game"),
    }
    if path not in allowed_paths or "\\" in destination or not destination.isprintable():
        return redirect(home)
    return redirect(destination)
