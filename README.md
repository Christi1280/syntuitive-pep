# SYNTUITIVE PEP

SYNTUITIVE PEP is a small Flask application for Grade 4–6 PEP preparation. The MVP contains three activities: flashcards, multiple-choice practice tests, and a landing page reserved for a future educational game. Grade selection is kept in the Flask session; activity results are not persisted.

## Requirements

- Python 3.10 or newer
- Flask (installed from `requirements.txt`)

## Install and run

From the repository root, create and activate a virtual environment, then install Flask:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python run.py
```

Open <http://127.0.0.1:5000/>. The Flask development server is for local development only.

## Tests

Run the route, curriculum-selector, activity-content, assessment-data, calculation, interaction-hook, navigation-link, and static-asset checks with:

```powershell
python -m unittest discover -s tests
```

## Project structure

- `app/__init__.py` creates the Flask application and registers the MVP routes.
- `app/routes/` contains the homepage/grade-selection routes and the three activity routes.
- `app/data/curriculum.py` retains the centralized grade → subject → topic curriculum structure. Categories are illustrative and not a verified official curriculum map.
- `app/data/activities.py` contains the sample flashcards and practice question.
- `app/data/assessments/g6_math_2025.py` contains the March 2025 Grade 6 Mathematics Performance Task data and calculated answer explanations.
- `app/templates/` contains the shared layout, homepage, flashcards, practice test, and future-game landing page.
- `app/static/css/styles.css` provides responsive layouts for phones, tablets, and desktops.
- `app/static/js/` contains the interactive flashcard and paginated practice-test behavior.
- `app/static/images/assessment/` contains the map, trip graph, and vehicle diagrams used by the Grade 6 Mathematics assessment.
- `app/models/` remains reserved for future persistence models; no database is configured.

The game page is an integration point only; it does not implement gameplay. The assessment's answer explanations are calculated from the information shown in the task and are not an official answer key. There is no authentication, account system, progress tracking, database, or persistent quiz history. Grade 4 and 5 activity content, and non-mathematics Grade 6 practice questions, have not yet been added. Set `FLASK_SECRET_KEY` to a private random value outside local development.
