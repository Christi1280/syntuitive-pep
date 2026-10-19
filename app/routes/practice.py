from flask import Blueprint, render_template, request, session

from app.data.activities import FLASHCARDS, PRACTICE_TESTS
from app.data.assessments.g6_math_2025 import ASSESSMENT as G6_MATH_2025
from app.data.curriculum import DEFAULT_GRADE, get_subject, get_subjects

practice_bp = Blueprint("practice", __name__)


def _selected_subject(grade):
    subjects = get_subjects(grade)
    subject_slug = request.args.get("subject", "")
    subject = get_subject(grade, subject_slug) if subject_slug else None
    default_subject = get_subject(grade, "mathematics") or subjects[0]
    return subjects, subject or default_subject


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
    assessment = None
    if grade == G6_MATH_2025["grade"] and subject["slug"] == G6_MATH_2025["subject"]:
        assessment = G6_MATH_2025
        questions = assessment["questions"]
    else:
        questions = PRACTICE_TESTS.get(grade, {}).get(subject["slug"], [])
        if questions:
            assessment = {
                "id": f"grade-{grade}-{subject['slug']}-sample",
                "title": f"{subject['name']} sample test",
                "description": "Answer the sample multiple-choice question.",
                "answer_key_note": "",
                "parts": {1: "Practice"},
                "questions": [
                    {
                        "id": f"sample-{index + 1}",
                        "part": 1,
                        "label": f"Question {index + 1}",
                        "type": "multiple_choice",
                        "question": question["question"],
                        "options": [
                            {"value": str(option_index), "text": option}
                            for option_index, option in enumerate(question["choices"])
                        ],
                        "correct_answer": str(question["correct_index"]),
                        "explanation": question["explanation"],
                    }
                    for index, question in enumerate(questions)
                ],
            }
    return render_template(
        "practice.html",
        title="Practice Tests",
        active_page="Practice Tests",
        grade=grade,
        subjects=subjects,
        subject=subject,
        questions=questions,
        assessment=assessment,
    )


@practice_bp.get("/game")
def game():
    return render_template("game.html", title="Play Game", active_page="Game")
