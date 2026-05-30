import importlib.util
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "course-ppt-review-html" / "scripts" / "build_review_page.py"


def load_module():
    spec = importlib.util.spec_from_file_location("build_review_page", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def sample_spec(image_name: str = "slide-01.jpg"):
    return {
        "course_title": "Demo Course",
        "module_title": "Demo Module",
        "module_subtitle": "Fixed quality review page",
        "learner_profile": "Chinese learner preparing an English oral exam.",
        "source_summary": [
            {"label": "Primary source", "text": "demo.pdf, slides 1-3.", "source": "Course source: slides 1-3."}
        ],
        "module_nav": [{"label": "Demo Module", "href": "demo.html", "sub": "current", "current": True}],
        "logic_map": [
            {"label": "Slides 1-3", "title": "Main chain", "text": "Start from symptoms, then choose a test.", "source": "Course source: slides 1-3."}
        ],
        "visuals": [
            {
                "slide": "Slide 1",
                "image": image_name,
                "alt": "Demo slide",
                "title": "Reasoning diagram",
                "what": "This slide teaches the diagnostic reasoning chain.",
                "how": "Read the arrows from presentation to syndrome and test choice.",
                "remember": "Define the syndrome before selecting complementary exams.",
                "exam_sentence": "A targeted exam should test the clinical hypothesis.",
                "dont_confuse": "Do not order tests before defining the syndrome.",
                "source": "Course source: slide 1.",
            }
        ],
        "terms": [
            {
                "group": "Clinical reasoning",
                "term": "syndrome",
                "zh": "综合征",
                "explanation_en": "A syndrome is a coherent pattern of signs and symptoms.",
                "explanation_zh": "综合征是一组相互关联的体征和症状模式。",
                "source": "Course source: slide 1.",
            },
            {
                "group": "Clinical reasoning",
                "term": "hypothesis",
                "zh": "假设",
                "explanation_en": "A hypothesis guides the choice of targeted tests.",
                "explanation_zh": "临床假设会指导有针对性的检查选择。",
                "source": "Course source: slide 2.",
            },
        ],
        "short_answers": [
            {
                "title": "How to choose a complementary exam",
                "answer_en": "I first define the syndrome, then choose the exam that directly tests the most likely hypothesis.",
                "answer_zh": "我会先定义综合征，再选择能直接检验最可能假设的检查。",
                "source": "Course source: slides 1-3.",
                "keywords": ["syndrome", "hypothesis", "exam choice"],
            }
        ],
        "comparisons": [
            {
                "title": "EEG vs MRI",
                "columns": ["Tool", "Use"],
                "rows": [["EEG", "Functional epileptic activity"], ["MRI", "Structural lesion"]],
                "source": "Course source: slides 2-3.",
            }
        ],
        "confusions": [
            {
                "title": "Test choice",
                "wrong": "Start with every available test.",
                "right": "Start with the syndrome and choose targeted tests.",
                "source": "Course source: slide 2.",
            }
        ],
        "review_order": [{"title": "First pass", "items": ["Read the logic map.", "Drill the short answer."]}],
    }


class BuildReviewPageTests(unittest.TestCase):
    def test_render_and_audit_fixed_structure(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "slide-01.jpg").write_bytes(b"fake image bytes")
            html_path = tmp_path / "demo.html"
            html_path.write_text(module.render_html(sample_spec()), encoding="utf-8")
            metrics = module.collect_metrics(html_path)
            self.assertEqual(metrics.term_cards, 2)
            self.assertEqual(metrics.answer_cards, 1)
            self.assertEqual(metrics.explain_items, 3)
            self.assertEqual(metrics.exam_lines, 1)
            self.assertFalse(metrics.broken_images)
            args = Namespace(
                min_nav_links=1,
                require_nav=True,
                min_visuals=1,
                min_terms=2,
                min_answers=1,
                min_explain_items=3,
                min_exam_lines=1,
                min_zh_blocks=1,
                min_source_labels=4,
                require_chinese=True,
                min_chinese_chars=10,
            )
            self.assertEqual(module.audit_metrics(metrics, args), [])

    def test_audit_rejects_summary_page_without_learning_affordances(self):
        module = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            html_path = Path(tmp) / "weak.html"
            html_path.write_text("<html><body><h1>Summary</h1><p>Only a plain summary.</p></body></html>", encoding="utf-8")
            metrics = module.collect_metrics(html_path)
            args = Namespace(
                min_nav_links=1,
                require_nav=True,
                min_visuals=1,
                min_terms=1,
                min_answers=1,
                min_explain_items=1,
                min_exam_lines=1,
                min_zh_blocks=1,
                min_source_labels=1,
                require_chinese=True,
                min_chinese_chars=10,
            )
            failures = module.audit_metrics(metrics, args)
            self.assertTrue(any("term_cards" in failure for failure in failures))
            self.assertTrue(any("answer_cards" in failure for failure in failures))
            self.assertTrue(any("exam_lines" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
