from flask import Blueprint, render_template, request, session

from app.data.activities import FLASHCARDS
from app.data.assessments import ASSESSMENTS
from app.data.curriculum import DEFAULT_GRADE, get_subject, get_subjects

practice_bp = Blueprint("practice", __name__)


def _selected_subject(grade):
    subjects = get_subjects(grade)
    subject = get_subject(grade, request.args.get("subject", ""))
    return subjects, subject or get_subject(grade, "mathematics") or subjects[0]


@practice_bp.get("/flashcards")
def flashcards():
    grade = session.get("grade", DEFAULT_GRADE)
    subjects, subject = _selected_subject(grade)
    cards = FLASHCARDS.get(grade, {}).get(subject["slug"], [])
    return render_template(
        "flashcards.html",
        title="Flashcards",
        active_page="Flashcards",
        grade=grade,
        subjects=subjects,
        subject=subject,
        cards=cards,
    )


@practice_bp.get("/practice")
def practice():
    grade = session.get("grade", DEFAULT_GRADE)
    subjects, subject = _selected_subject(grade)
    return render_template(
        "practice.html",
        title="Practice Tests",
        active_page="Practice Tests",
        grade=grade,
        subjects=subjects,
        subject=subject,
        assessment=ASSESSMENTS.get((grade, subject["slug"])),
    )


@practice_bp.get("/game")
def game():
    return render_template("game.html", title="Play Game", active_page="Game")
