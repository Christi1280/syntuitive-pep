from flask import Blueprint, redirect, render_template, session, url_for

from app.data.curriculum import DEFAULT_GRADE
practice_bp = Blueprint("practice", __name__)


@practice_bp.get("/practice")
def practice():
    grade = session.get("grade", DEFAULT_GRADE)
    return render_template(
        "practice.html",
        title="Practice Test Center",
        active_page="Practice Tests",
        grade=grade,
    )


@practice_bp.get("/practice/demo")
def demo():
    if session.get("grade", DEFAULT_GRADE) != 6:
        return redirect(url_for("practice.practice"))
    return render_template("quiz.html", title="Mathematics practice", active_page="Practice Tests")


@practice_bp.get("/flashcards")
def flashcards():
    return render_template("flashcards.html", title="Flashcards", active_page="Flashcards")


@practice_bp.get("/quiz-arena")
def quiz_arena():
    return render_template("quiz_arena.html", title="Quiz Arena", active_page="Quiz Arena")


@practice_bp.get("/past-papers")
def past_papers():
    return render_template(
        "past_papers.html",
        title="Past Paper Library",
        active_page="Practice Tests",
        grade=session.get("grade", DEFAULT_GRADE),
    )


@practice_bp.get("/mock-exams")
def mock_exams():
    return render_template(
        "mock_exams.html",
        title="Mock Examinations",
        active_page="Practice Tests",
        grade=session.get("grade", DEFAULT_GRADE),
    )
