from flask import Blueprint, abort, redirect, render_template, request, session, url_for
from urllib.parse import urlsplit, urlunsplit

from app.data.curriculum import DEFAULT_GRADE, is_supported_grade

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
    try:
        grade = int(request.form.get("grade", ""))
    except ValueError:
        abort(400)
    if not is_supported_grade(grade):
        abort(400)

    session["grade"] = grade
    destination = request.form.get("return_to", url_for("main.index"))
    parsed_destination = urlsplit(destination)
    allowed_paths = {"/", "/flashcards", "/practice", "/game"}
    if (
        parsed_destination.scheme
        or parsed_destination.netloc
        or parsed_destination.path not in allowed_paths
        or "\\" in destination
    ):
        return redirect(url_for("main.index"))
    return redirect(urlunsplit(("", "", parsed_destination.path, parsed_destination.query, "")))
