from flask import Blueprint, abort, redirect, render_template, session, url_for

from app.data.curriculum import (
    DEFAULT_GRADE,
    get_subject,
    get_subjects,
    get_topic,
    is_supported_grade,
)

learning_bp = Blueprint("learning", __name__)


@learning_bp.get("/learning")
def learning():
    return redirect(url_for("learning.grade_learning", grade=session.get("grade", DEFAULT_GRADE)))


@learning_bp.get("/learning/<int:grade>")
def grade_learning(grade):
    if not is_supported_grade(grade):
        abort(404)
    session["grade"] = grade
    return render_template(
        "learning.html",
        title=f"Grade {grade} Learning Center",
        active_page="Learning Center",
        grade=grade,
        subjects=get_subjects(grade),
    )


def _render_subject(grade, subject_slug):
    if not is_supported_grade(grade):
        abort(404)
    selected_subject = get_subject(grade, subject_slug)
    if selected_subject is None:
        abort(404)
    session["grade"] = grade
    return render_template(
        "subject.html",
        title=selected_subject["name"],
        active_page="Learning Center",
        grade=grade,
        subject=selected_subject,
    )


@learning_bp.get("/learning/<int:grade>/<subject_slug>")
def grade_subject(grade, subject_slug):
    return _render_subject(grade, subject_slug)


@learning_bp.get("/learning/<int:grade>/<subject_slug>/<topic_slug>")
def grade_lesson(grade, subject_slug, topic_slug):
    if not is_supported_grade(grade):
        abort(404)
    selected_subject = get_subject(grade, subject_slug)
    if selected_subject is None:
        abort(404)
    selected_topic = get_topic(selected_subject, topic_slug)
    if selected_topic is None:
        abort(404)
    session["grade"] = grade
    return render_template(
        "lesson.html",
        title=selected_topic["name"],
        active_page="Learning Center",
        grade=grade,
        subject=selected_subject,
        topic=selected_topic,
    )


@learning_bp.get("/learning/<subject_slug>")
def legacy_subject(subject_slug):
    return _render_subject(session.get("grade", DEFAULT_GRADE), subject_slug)


@learning_bp.get("/learning/<subject_slug>/<topic_slug>")
def legacy_lesson(subject_slug, topic_slug):
    grade = session.get("grade", DEFAULT_GRADE)
    selected_subject = get_subject(grade, subject_slug)
    if selected_subject is None:
        abort(404)
    selected_topic = get_topic(selected_subject, topic_slug)
    if selected_topic is None:
        abort(404)
    return redirect(
        url_for(
            "learning.grade_lesson",
            grade=grade,
            subject_slug=subject_slug,
            topic_slug=topic_slug,
        )
    )
