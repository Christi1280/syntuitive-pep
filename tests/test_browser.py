import os
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread

from flask import send_file
from werkzeug.serving import make_server

from app import create_app


class BrowserTests(unittest.TestCase):
    @unittest.skipUnless(
        os.environ.get("PEP_TEST_BROWSER"), "Set PEP_TEST_BROWSER to a Chromium executable"
    )
    def test_flashcards_and_practice(self):
        app = create_app(local=True)
        harness = Path(__file__).with_name("browser_interactions.html").resolve()
        app.add_url_rule("/browser-checks", view_func=lambda: send_file(harness))
        server = make_server("127.0.0.1", 0, app, threaded=True)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(thread.join)
        self.addCleanup(server.shutdown)

        with TemporaryDirectory(ignore_cleanup_errors=True) as profile:
            command = [
                os.environ["PEP_TEST_BROWSER"],
                "--headless",
                "--disable-gpu",
                "--disable-software-rasterizer",
                "--no-first-run",
                "--disable-background-networking",
                f"--user-data-dir={profile}",
                "--dump-dom",
                "--virtual-time-budget=8000",
                f"http://127.0.0.1:{server.server_port}/browser-checks",
            ]
            browser = subprocess.run(
                command, capture_output=True, encoding="utf-8", errors="replace", timeout=40
            )
        self.assertEqual(browser.returncode, 0, browser.stderr)
        result = next((line for line in browser.stdout.splitlines() if 'id="result"' in line), "")
        self.assertIn('<output id="result">Passed</output>', result)
