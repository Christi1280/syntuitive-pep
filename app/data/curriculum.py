"""Prototype curriculum organization; categories are not an official curriculum map."""

import re


DEFAULT_GRADE = 6


def _topic(name):
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return {
        "name": name,
        "slug": slug,
        "lessons": [],
    }


def _subject(name, slug, icon, color="", topics=()):
    return {
        "name": name,
        "slug": slug,
        "icon": icon,
        "color": color,
        "topics": [_topic(topic) for topic in topics],
    }


CURRICULUM = {
    4: {
        "grade": 4,
        "subjects": [
            _subject("Literacy", "literacy", "📚"),
            _subject("Numeracy", "numeracy", "📐"),
        ],
    },
    5: {
        "grade": 5,
        "subjects": [
            _subject("Language Arts", "language-arts", "📚"),
            _subject("Mathematics", "mathematics", "📐"),
        ],
    },
    6: {
        "grade": 6,
        "subjects": [
            _subject(
                "Language Arts", "language-arts", "📚", "peach",
                ("Reading Comprehension", "Grammar", "Vocabulary", "Writing Skills"),
            ),
            _subject(
                "Mathematics", "mathematics", "📐",
                topics=("Number Operations", "Fractions", "Decimals", "Measurement", "Geometry", "Data Handling"),
            ),
            _subject(
                "Science", "science", "🔬", "mint",
                ("Living Things", "Matter & Energy", "Earth & Space", "Forces & Motion"),
            ),
            _subject(
                "Social Studies", "social-studies", "🌎", "purple",
                ("Jamaican Heritage", "Geography", "Citizenship", "Communities"),
            ),
            _subject(
                "Ability Test", "ability-test", "🧠", "yellow",
                ("Verbal Reasoning", "Number Patterns", "Logical Thinking", "Problem Solving"),
            ),
        ],
    },
}

SUPPORTED_GRADES = tuple(CURRICULUM)


def is_supported_grade(grade):
    return type(grade) is int and grade in CURRICULUM


def get_subjects(grade):
    if not is_supported_grade(grade):
        return None
    return CURRICULUM[grade]["subjects"]


def get_subject(grade, subject_slug):
    subjects = get_subjects(grade)
    if subjects is None:
        return None
    return next((subject for subject in subjects if subject["slug"] == subject_slug), None)
