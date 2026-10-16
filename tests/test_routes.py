import unittest
from html.parser import HTMLParser
from urllib.parse import urlparse

from app import create_app
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


class GradeAwareRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app({"TESTING": True, "SECRET_KEY": "test-secret"}).test_client()

    def test_all_existing_pages_and_grade_pages_render(self):
        paths = [
            "/", "/dashboard", "/learning", "/learning/mathematics",
            "/learning/mathematics/fractions", "/learning/4", "/learning/5",
            "/learning/6", "/practice", "/practice/demo", "/flashcards",
            "/quiz-arena", "/progress", "/achievements", "/settings",
            "/past-papers", "/mock-exams", "/admin", "/admin/lessons",
            "/admin/questions", "/admin/tests",
        ]
        for grade, grade_data in CURRICULUM.items():
            paths.extend(
                f"/learning/{grade}/{subject['slug']}"
                for subject in grade_data["subjects"]
            )
            for subject in grade_data["subjects"]:
                paths.extend(
                    f"/learning/{grade}/{subject['slug']}/{topic['slug']}"
                    for topic in subject["topics"]
                )

        for path in paths:
            with self.subTest(path=path):
                response = self.client.get(path, follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b"SYNTUITIVE", response.data)
                response.close()

    def test_grade_selection_defaults_to_six_and_persists(self):
        response = self.client.get("/dashboard")
        self.assertIn(b"Welcome to Grade 6", response.data)
        self.assertIn(b"Grade 6 Subjects", response.data)
        response.close()

        response = self.client.post("/grade", data={"grade": "4"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/dashboard")
        response.close()

        dashboard = self.client.get("/dashboard")
        learning = self.client.get("/learning")
        self.assertIn(b"Welcome to Grade 4", dashboard.data)
        self.assertIn(b"Grade 4 Subjects", dashboard.data)
        self.assertIn(b"Literacy", dashboard.data)
        self.assertIn(b"Numeracy", dashboard.data)
        self.assertNotIn(b"Science", dashboard.data)
        self.assertEqual(learning.status_code, 302)
        self.assertEqual(learning.headers["Location"], "/learning/4")
        dashboard.close()
        learning.close()

        progress = self.client.get("/progress")
        self.assertIn(b"GRADE 4 LEARNING JOURNEY", progress.data)
        progress.close()

    def test_grade_selector_is_in_shared_header_and_accepts_each_supported_grade(self):
        for grade in (4, 5, 6):
            with self.subTest(grade=grade):
                response = self.client.post("/grade", data={"grade": str(grade)})
                self.assertEqual(response.status_code, 302)
                response.close()
                page = self.client.get("/dashboard")
                self.assertIn(f'value="{grade}" selected'.encode(), page.data)
                self.assertIn(f"Welcome to Grade {grade}".encode(), page.data)
                page.close()

    def test_grade_categories_and_grade_six_topics_are_separate(self):
        expected_subjects = {
            4: (b"Literacy", b"Numeracy"),
            5: (b"Language Arts", b"Mathematics"),
            6: (b"Language Arts", b"Mathematics", b"Science", b"Social Studies", b"Ability Test"),
        }
        for grade, subjects in expected_subjects.items():
            with self.subTest(grade=grade):
                response = self.client.get(f"/learning/{grade}")
                for name in subjects:
                    self.assertIn(name, response.data)
                if grade != 6:
                    self.assertIn(b"coming soon", response.data.lower())
                    self.assertNotIn(b"Fractions", response.data)
                response.close()

        grade6_subject = self.client.get("/learning/6/mathematics")
        self.assertIn(b"Fractions", grade6_subject.data)
        self.assertIn(b"Placeholder topics", grade6_subject.data)
        grade6_subject.close()

        grade4_subject = self.client.get("/learning/4/literacy")
        self.assertIn(b"content is in development", grade4_subject.data)
        self.assertNotIn(b"Reading Comprehension", grade4_subject.data)
        grade4_subject.close()

        grade6_lesson = self.client.get("/learning/6/mathematics/fractions")
        self.assertIn(b"Let's learn: Fractions", grade6_lesson.data)
        grade6_lesson.close()

    def test_invalid_grade_subject_and_topic_urls_return_404(self):
        paths = [
            "/learning/3",
            "/learning/7/mathematics",
            "/learning/4/mathematics",
            "/learning/5/science",
            "/learning/6/literacy",
            "/learning/4/literacy/not-a-topic",
            "/learning/6/mathematics/not-a-topic",
            "/learning/not-a-subject",
        ]
        for path in paths:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 404)
                response.close()

    def test_demo_quiz_remains_grade_six_only(self):
        grade6_quiz = self.client.get("/practice/demo")
        self.assertEqual(grade6_quiz.status_code, 200)
        self.assertIn(b"What is", grade6_quiz.data)
        grade6_quiz.close()

        self.client.post("/grade", data={"grade": "5"}).close()
        practice = self.client.get("/practice")
        self.assertIn(b"Grade 5 practice is coming soon", practice.data)
        self.assertNotIn(b"Sample mathematics question", practice.data)
        practice.close()
        demo = self.client.get("/practice/demo")
        self.assertEqual(demo.status_code, 302)
        self.assertEqual(demo.headers["Location"], "/practice")
        demo.close()

    def test_invalid_grade_selection_is_rejected(self):
        for grade in ("3", "7", "not-a-grade", ""):
            with self.subTest(grade=grade):
                response = self.client.post("/grade", data={"grade": grade})
                self.assertEqual(response.status_code, 400)
                response.close()

    def test_static_assets_and_all_rendered_links_resolve(self):
        assets = (
            "/static/css/styles.css",
            "/static/js/main.js",
            "/static/js/practice.js",
            "/static/js/flashcards.js",
        )
        for path in assets:
            with self.subTest(asset=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                response.close()

        parser = LocalLinks()
        pages = ["/", "/dashboard", "/practice", "/flashcards", "/quiz-arena"]
        for grade, grade_data in CURRICULUM.items():
            pages.append(f"/learning/{grade}")
            pages.extend(
                f"/learning/{grade}/{subject['slug']}"
                for subject in grade_data["subjects"]
            )
            for subject in grade_data["subjects"]:
                pages.extend(
                    f"/learning/{grade}/{subject['slug']}/{topic['slug']}"
                    for topic in subject["topics"]
                )

        for page_path in pages:
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
