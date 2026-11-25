"""Practice assessments in the format used by the practice template."""

from app.data.assessments.g6_math_2025 import ASSESSMENT as GRADE_6_MATH_2025


# Preserve the original sample without displacing the full assessment.
FRACTIONS_SAMPLE = {
    "id": "grade-6-mathematics-sample",
    "title": "Mathematics sample test",
    "grade": 6,
    "subject": "mathematics",
    "description": "Answer the sample multiple-choice question.",
    "answer_key_note": "",
    "parts": {1: "Practice"},
    "questions": [
        {
            "id": "sample-1",
            "part": 1,
            "label": "Question 1",
            "type": "multiple_choice",
            "question": "What is ½ + ¼?",
            "options": [
                {"value": "A", "text": "2/6"},
                {"value": "B", "text": "3/4"},
                {"value": "C", "text": "1/6"},
                {"value": "D", "text": "2/4"},
            ],
            "correct_answer": "B",
            "explanation": "Rewrite ½ as 2/4. Then 2/4 + 1/4 = 3/4.",
        },
    ],
}

ASSESSMENTS = {
    (GRADE_6_MATH_2025["grade"], GRADE_6_MATH_2025["subject"]): GRADE_6_MATH_2025,
}
