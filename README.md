# SYNTUITIVE PEP

SYNTUITIVE PEP is a Flask/Jinja2 implementation of the existing responsive website design prototype. The public landing page, student portal, learning pages, practice experience, flashcards, and prototype administrator screens are included. Educational content and all backend account/content systems remain illustrative.

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

Run the route, template, navigation-link, and static-asset checks with:

```powershell
python -m unittest discover -s tests
```

## Project structure

- `app/__init__.py` creates the Flask application and registers blueprints.
- `app/routes/` contains route groups for the public site, learning, practice, student pages, and prototype admin pages.
- `app/data/curriculum.py` is the single grade → subject → topic → lessons data structure. Its assessment categories are illustrative and are not an official 2027 specification; unavailable lessons remain empty rather than fabricated.
- `app/templates/` contains separate Jinja2 templates with shared portal layout in `base.html`.
- `app/static/css/styles.css` is the original website stylesheet.
- `app/static/js/` contains shared navigation, demo quiz, and flashcard behavior.
- `app/models/` is reserved for future persistence models; no database is configured.
- `tests/` contains Flask route and asset tests.

## Prototype limitations

Student account/authentication, PostgreSQL, persistent learning content, real progress tracking, multiplayer, and content administration are not implemented. The Admin Studio and its subpages are publicly accessible design prototypes and **must not** be used to manage real content or considered secure. Do not expose this development application as a production service before authentication, authorization, secret management, and deployment hardening are implemented.

Quiz attempts are stored only in the current browser using localStorage. Subject topics and sample lesson text are illustrative, not a verified complete Jamaican PEP curriculum map. Google Fonts are used when online, with system font fallbacks.

The selected grade (default Grade 6) is stored in the Flask session cookie. The development app uses a local-only fallback secret; set `FLASK_SECRET_KEY` to a private random value for any non-development environment. Grades 4 and 5 currently expose their requested subject categories only, with topics, lessons, and practice material marked coming soon.
