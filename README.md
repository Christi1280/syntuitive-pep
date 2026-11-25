# SYNTUITIVE PEP

SYNTUITIVE PEP is an educational web application I am developing to help Jamaican primary school students prepare for their Primary Exit Profile (PEP) examinations.

The idea behind this project is to make studying more interactive and engaging through practice questions, flashcards, worked explanations, and educational games.

The project is currently in active development.

## Features

- **Grade selection:** Students can select Grade 4, 5, or 6 and browse subjects for their grade.
- **Flashcards:** Students can review concepts in Mathematics, Science, and Language Arts.
- **Practice assessments:** Interactive questions with scoring, answer explanations, and the option to retake assessments.
- **Game-based learning:** An integrated Unity WebGL game called PEP Space Race, designed to combine learning with gameplay.
- **Session management:** The website remembers the student's selected grade as they navigate between pages.

Most of the current learning content is focused on Grade 6, with plans to expand coverage across other grades and subjects.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Flask | Web application framework |
| Jinja | HTML templating |
| HTML & CSS | Website structure and styling |
| JavaScript | Interactive features and assessment scoring |
| Unity & C# | Educational game development |
| WebGL | Running the Unity game in the browser |
| Git & GitHub | Version control |

## How It Works

The website uses Flask to manage routes, load educational content, and render pages. JavaScript handles interactive features such as flipping flashcards, navigating between questions, calculating scores, and displaying feedback.

The project is organized into separate modules for routes, educational content, templates, and static files. This makes it easier to maintain the application and add new features as the platform grows.

The application also includes CSRF protection, signed session cookies, environment-based configuration, and automated tests.

## PEP Space Race

PEP Space Race is an educational game developed separately in Unity and integrated into the website using WebGL.

The concept is simple: players must answer PEP-style questions correctly to unlock doors and progress through a level. The goal is to reach the finish line before their opponent.

The game is still in development, with plans to introduce more questions, additional levels, and online multiplayer functionality.

## Running the Project Locally

Python 3.10 or newer is required.

Clone the repository:

```bash
git clone https://github.com/Christi1280/syntuitive-pep.git
cd syntuitive-pep
```

Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python run.py
```

Open the following address in your browser:

http://127.0.0.1:5000/

For production deployments, a private `FLASK_SECRET_KEY` must be configured through environment variables.

## Testing

The project includes automated tests covering:

- Grade and subject selection
- Assessment questions and answers
- Security and form validation
- Static file delivery
- Unity WebGL integration

Optional browser tests also cover flashcard interactions, assessment navigation, scoring, and retakes.

To run the tests:

```bash
python -m unittest discover -s tests
```

## Future Development

There are several features I plan to introduce as the project develops:

- More learning content across Grades 4, 5, and 6
- Original PEP-style practice assessments
- Student accounts
- Saved assessment results and progress tracking
- Additional educational games
- Online multiplayer
- Improved mobile support and accessibility

## Educational Content and Third-Party Assets

The existing PEP examination questions and diagrams are being used as temporary placeholder content while I develop and test the platform.

The intended production release will feature original PEP-style questions developed specifically for the application and aligned with the Jamaican primary school curriculum.

PEP Space Race also uses third-party assets obtained from the Unity Asset Store. All third-party materials remain subject to their respective copyrights and license terms. Redistribution permissions have not yet been fully verified.

This is an independent project and is not officially affiliated with or endorsed by any examination authority.

## Author

**Christian Williams**

Software Developer | Georgia State University Graduate

Developed under **SYNTUITIVE**.

- [GitHub](https://github.com/Christi1280)
- [LinkedIn](https://www.linkedin.com/in/christianwilliams1280/)
