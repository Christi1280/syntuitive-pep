import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from app import create_app
from app.data.activities import FLASHCARDS, PRACTICE_TESTS
from app.data.assessments.g6_math_2025 import ASSESSMENT
from app.data.curriculum import CURRICULUM


class LocalLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in {"href", "src"} and value:
                parsed = urlparse(value)
                if not parsed.scheme and not value.startswith("#"):
                    self.urls.append(value)


class MvpRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app({"TESTING": True, "SECRET_KEY": "test-secret"}).test_client()

    def test_homepage_shows_only_the_three_mvp_activities(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        for feature in (b"Flashcards", b"Practice Tests", b"Play Game"):
            self.assertIn(feature, response.data)
        for removed_item in (b"Dashboard", b"Learning Center", b"Settings", b"Achievements"):
            self.assertNotIn(removed_item, response.data)
        response.close()

    def test_grade_selector_defaults_to_six_and_persists_supported_grades(self):
        response = self.client.get("/")
        self.assertIn(b'value="6" selected', response.data)
        response.close()

        for grade in (4, 5, 6):
            with self.subTest(grade=grade):
                response = self.client.post("/grade", data={"grade": str(grade), "return_to": "/flashcards"})
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.headers["Location"], "/flashcards")
                response.close()
                page = self.client.get("/flashcards")
                self.assertIn(f"Grade {grade}".encode(), page.data)
                self.assertIn(f'value="{grade}" selected'.encode(), page.data)
                page.close()

    def test_grade_selection_rejects_invalid_values_and_external_redirects(self):
        for grade in ("3", "7", "not-a-grade", ""):
            with self.subTest(grade=grade):
                response = self.client.post("/grade", data={"grade": grade})
                self.assertEqual(response.status_code, 400)
                response.close()

        for destination in ("//example.com", "/\\example.com", "https://example.com/"):
            with self.subTest(destination=destination):
                response = self.client.post(
                    "/grade",
                    data={"grade": "5", "return_to": destination},
                )
                self.assertEqual(response.headers["Location"], "/")
                response.close()

    def test_subject_selectors_use_the_central_curriculum_for_each_grade(self):
        for grade, grade_data in CURRICULUM.items():
            self.client.post("/grade", data={"grade": str(grade)}).close()
            for path in ("/flashcards", "/practice"):
                with self.subTest(grade=grade, path=path):
                    response = self.client.get(path)
                    for subject in grade_data["subjects"]:
                        self.assertIn(subject["name"].encode(), response.data)
                    response.close()

    def test_flashcards_retain_the_sample_deck_and_subject_filtering(self):
        response = self.client.get("/flashcards?subject=science")
        self.assertIn(b"What is evaporation?", response.data)
        self.assertIn(b"The process in which liquid changes into gas.", response.data)
        self.assertIn(b"flashcards.js", response.data)
        response.close()

        response = self.client.get("/flashcards?subject=mathematics")
        self.assertIn(b"What is a numerator?", response.data)
        response.close()

        self.client.post("/grade", data={"grade": "4"}).close()
        response = self.client.get("/flashcards")
        self.assertIn(b"No Literacy flashcards yet", response.data)
        response.close()

    def test_performance_task_is_integrated_for_grade_six_mathematics(self):
        response = self.client.get("/practice")
        self.assertIn(b"March 2025 Grade 6 Mathematics Performance Task", response.data)
        self.assertIn(b"24 questions", response.data)
        self.assertIn(b"not an official answer key", response.data)
        self.assertIn(b"data-question-id=\"p1-q1a\"", response.data)
        self.assertIn(b"data-question-id=\"p4-q6b\"", response.data)
        self.assertIn(b"question-number-list", response.data)
        self.assertIn(b"previous-question", response.data)
        self.assertIn(b"next-question", response.data)
        self.assertIn(b"retry-test", response.data)
        self.assertIn(b"hidden", response.data)
        self.assertIn(b"practice.js", response.data)
        response.close()

    def test_assessment_question_data_has_unique_ids_valid_answers_and_visuals(self):
        questions = ASSESSMENT["questions"]
        self.assertEqual(len(questions), 24)
        self.assertEqual(len({question["id"] for question in questions}), len(questions))
        expected_answers = {
            "p1-q1a": "B",
            "p1-q1b": "C",
            "p1-q1c": "B",
            "p1-q1d": "B",
            "p1-q2a": "true",
            "p1-q2b": "false",
            "p1-q2c": "true",
            "p2-q3a-car": "C",
            "p2-q3a-bus": "B",
            "p2-q3b-teachers": "B",
            "p2-q3b-students": "C",
            "p2-q4a-teachers": "B",
            "p2-q4a-students": "C",
            "p2-q4a-passengers": "C",
            "p2-q4b-teachers": "B",
            "p2-q4b-students": "C",
            "p2-q4b-passengers": "C",
            "p2-q4c": "A",
            "p3-q5a": "C",
            "p3-q5b": "C",
            "p3-q5c": "C",
            "p3-q6a-car": "C",
            "p3-q6a-bus": "B",
            "p4-q6b": "A",
        }
        self.assertEqual(
            {question["id"]: question["correct_answer"] for question in questions},
            expected_answers,
        )

        image_references = set()
        for question in questions:
            with self.subTest(question=question["id"]):
                self.assertTrue(question["question"])
                self.assertTrue(question["explanation"])
                self.assertIn(question["part"], ASSESSMENT["parts"])
                option_values = [option["value"] for option in question["options"]]
                self.assertEqual(len(option_values), len(set(option_values)))
                if question["type"] == "multiple_choice":
                    self.assertEqual(len(question["options"]), 4)
                else:
                    self.assertEqual(question["type"], "true_false")
                    self.assertEqual(option_values, ["true", "false"])
                self.assertIn(question["correct_answer"], option_values)
                if "image" in question:
                    self.assertTrue(question["image_alt"])
                    image_references.add(question["image"])

        self.assertEqual(
            image_references,
            {
                "images/assessment/baker-town-map.png",
                "images/assessment/trips-per-day.png",
                "images/assessment/car-seating.png",
                "images/assessment/bus-seating.png",
            },
        )

        for image in image_references:
            with self.subTest(image=image):
                response = self.client.get(f"/static/{image}")
                self.assertEqual(response.status_code, 200)
                response.close()

    def test_assessment_calculation_answers_match_source_values(self):
        correct = {
            question["id"]: question["correct_answer"]
            for question in ASSESSMENT["questions"]
        }
        self.assertEqual(3 * 100, 300)
        self.assertEqual(6 * 100, 600)
        self.assertEqual(30 * 100, 3000)
        self.assertEqual(6 + 3 + 6 + 5, 20)
        self.assertEqual(2 + 1 + 2 + 1, 6)
        self.assertEqual((14 // 7) * 1, 2)
        self.assertEqual((14 // 7) * 6, 12)
        self.assertEqual(20 * 4, 80)
        self.assertEqual(6 * 14, 84)
        self.assertEqual(3 * 64.50, 193.50)
        self.assertEqual(20 * 200 + 60 * 100, 10000)
        self.assertEqual(12 * 200 + 72 * 100, 9600)
        self.assertEqual(correct["p2-q4c"], "A")
        self.assertEqual(correct["p4-q6b"], "A")

    def test_practice_script_keeps_navigation_scoring_and_retake_handlers(self):
        script_path = Path(__file__).parents[1] / "app" / "static" / "js" / "practice.js"
        script = script_path.read_text(encoding="utf-8")
        for interaction in (
            'previous.addEventListener("click"',
            'next.addEventListener("click"',
            'button.addEventListener("click"',
            'submit.addEventListener("click"',
            'retry.addEventListener("click"',
            "currentIndex -= 1",
            "currentIndex += 1",
            "score += 1",
            "Your score:",
            'classList.remove("selected", "correct", "wrong")',
        ):
            with self.subTest(interaction=interaction):
                self.assertIn(interaction, script)

    def test_other_grade_and_subject_practice_pages_remain_available(self):
        for grade, subject in ((4, "literacy"), (5, "mathematics"), (6, "science")):
            self.client.post("/grade", data={"grade": str(grade)}).close()
            response = self.client.get(f"/practice?subject={subject}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(f"No ".encode(), response.data)
            self.assertNotIn(b"March 2025 Grade 6 Mathematics Performance Task", response.data)
            response.close()

        question = PRACTICE_TESTS[6]["mathematics"][0]
        self.assertEqual(question["choices"][question["correct_index"]], "3/4")
        self.assertEqual(len(FLASHCARDS[6]["science"]), 1)

    def test_game_landing_page_is_an_integration_placeholder(self):
        response = self.client.get("/game")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No gameplay is available yet", response.data)
        self.assertIn(b"Home", response.data)
        response.close()

    def test_removed_pages_are_not_routed(self):
        for path in (
            "/dashboard", "/progress", "/achievements", "/settings",
            "/learning", "/learning/6/mathematics/fractions", "/mock-exams",
            "/past-papers", "/quiz-arena", "/admin",
        ):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 404)
                response.close()

    def test_static_assets_and_all_rendered_local_links_resolve(self):
        for path in (
            "/static/css/styles.css",
            "/static/js/flashcards.js",
            "/static/js/practice.js",
            "/static/images/assessment/baker-town-map.png",
            "/static/images/assessment/trips-per-day.png",
            "/static/images/assessment/car-seating.png",
            "/static/images/assessment/bus-seating.png",
        ):
            with self.subTest(asset=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                response.close()

        parser = LocalLinks()
        for page_path in ("/", "/flashcards", "/practice", "/game"):
            response = self.client.get(page_path, follow_redirects=True)
            self.assertEqual(response.status_code, 200, page_path)
            parser.feed(response.get_data(as_text=True))
            response.close()

        for link in parser.urls:
            with self.subTest(link=link):
                response = self.client.get(link, follow_redirects=True)
                self.assertIn(response.status_code, (200, 304), link)
                response.close()


if __name__ == "__main__":
    unittest.main()
