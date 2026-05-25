import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "course-ppt-review-html" / "scripts" / "prepare_ppt_review_assets.py"


def load_module():
    spec = importlib.util.spec_from_file_location("prepare_ppt_review_assets", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PrepareAssetsTests(unittest.TestCase):
    def test_parse_pages(self):
        module = load_module()
        self.assertEqual(module.parse_pages("3,4,7-9,9"), [3, 4, 7, 8, 9])

    def test_visual_snippets(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "snippets.html"
            module.write_visual_snippets(path, [{"page": 3, "file": "demo-slide-03.jpg", "bytes": 123}])
            text = path.read_text(encoding="utf-8")
            self.assertIn("visual-card", text)
            self.assertIn("demo-slide-03.jpg", text)
            self.assertIn("Exam sentence", text)


if __name__ == "__main__":
    unittest.main()
