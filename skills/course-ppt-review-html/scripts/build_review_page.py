#!/usr/bin/env python3
"""Build and audit exam-oriented bilingual slide review HTML pages.

This harness keeps page quality stable by separating content generation from
page construction:

1. An agent fills a structured JSON spec.
2. This script renders the spec with a fixed HTML layout.
3. This script audits the output and fails when core learning affordances drift.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


PLACEHOLDER_PATTERNS = [
    "TO" + "DO",
    "TBD",
    "Add a memory title",
    "Explain what this PPT page is teaching",
    "Add a complete",
    "placeholder",
    "lorem ipsum",
]


REQUIRED_VISUAL_FIELDS = [
    "image",
    "title",
    "what",
    "how",
    "remember",
    "exam_sentence",
    "dont_confuse",
    "source",
]

REQUIRED_TERM_FIELDS = ["term", "zh", "explanation_en", "explanation_zh", "source"]
REQUIRED_ANSWER_FIELDS = ["title", "answer_en", "answer_zh", "source"]


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Spec must be a JSON object: {path}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def text(value: Any) -> str:
    return str(value or "").strip()


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "item"


def missing_fields(item: dict[str, Any], fields: list[str]) -> list[str]:
    return [field for field in fields if not text(item.get(field))]


def validate_spec(spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field_name in ["course_title", "module_title"]:
        if not text(spec.get(field_name)):
            errors.append(f"Missing required top-level field: {field_name}")

    required_lists = [
        "source_summary",
        "logic_map",
        "visuals",
        "terms",
        "short_answers",
        "confusions",
        "review_order",
    ]
    for field_name in required_lists:
        if not as_list(spec.get(field_name)):
            errors.append(f"Missing or empty required list: {field_name}")

    for index, item in enumerate(as_list(spec.get("visuals")), 1):
        if not isinstance(item, dict):
            errors.append(f"visuals[{index}] must be an object")
            continue
        missing = missing_fields(item, REQUIRED_VISUAL_FIELDS)
        if missing:
            errors.append(f"visuals[{index}] missing fields: {', '.join(missing)}")

    for index, item in enumerate(as_list(spec.get("terms")), 1):
        if not isinstance(item, dict):
            errors.append(f"terms[{index}] must be an object")
            continue
        missing = missing_fields(item, REQUIRED_TERM_FIELDS)
        if missing:
            errors.append(f"terms[{index}] missing fields: {', '.join(missing)}")

    for index, item in enumerate(as_list(spec.get("short_answers")), 1):
        if not isinstance(item, dict):
            errors.append(f"short_answers[{index}] must be an object")
            continue
        missing = missing_fields(item, REQUIRED_ANSWER_FIELDS)
        if missing:
            errors.append(f"short_answers[{index}] missing fields: {', '.join(missing)}")

    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.lower() in json.dumps(spec, ensure_ascii=False).lower():
            errors.append(f"Placeholder text remains in spec: {pattern}")

    return errors


def default_spec() -> dict[str, Any]:
    return {
        "course_title": "Course Title",
        "module_title": "Module Title",
        "module_subtitle": "Exam-oriented bilingual review page",
        "learner_profile": "Chinese native speaker revising an English/French-taught course.",
        "source_summary": [
            {
                "label": "Primary source",
                "text": "Source PDF or PPT name, slide range.",
                "source": "Course source: slides X-Y.",
            }
        ],
        "stats": [
            {"value": "0", "label": "source slides"},
            {"value": "0", "label": "visual explanations"},
            {"value": "0", "label": "terms"},
            {"value": "0", "label": "short answers"},
        ],
        "module_nav": [],
        "logic_map": [
            {
                "label": "Slides X-Y",
                "title": "Core logic step",
                "text": "Explain how this slide range fits the module argument.",
                "source": "Course source: slides X-Y.",
            }
        ],
        "visuals": [],
        "terms": [],
        "short_answers": [],
        "comparisons": [],
        "confusions": [
            {
                "title": "Common confusion",
                "wrong": "State the tempting but wrong interpretation.",
                "right": "State the corrected exam-ready interpretation.",
                "source": "Course source: slides X-Y.",
            }
        ],
        "review_order": [
            {
                "title": "First pass",
                "items": ["Learn the logic map.", "Read visual explanations.", "Drill short answers."],
            }
        ],
    }


def init_spec(args: argparse.Namespace) -> None:
    spec = default_spec()
    spec["course_title"] = args.course_title
    spec["module_title"] = args.module_title
    spec["module_subtitle"] = args.module_subtitle

    rendered: list[dict[str, Any]] = []
    if args.manifest:
        manifest = load_json(Path(args.manifest))
        rendered = as_list(manifest.get("rendered"))
        source_pdf = text(manifest.get("source_pdf"))
        total_pages = manifest.get("total_pages", "")
        spec["source_summary"] = [
            {
                "label": "Primary source",
                "text": f"{Path(source_pdf).name if source_pdf else 'Source PDF'}, slides 1-{total_pages}.",
                "source": f"Course source: {Path(source_pdf).name if source_pdf else 'source slides'}.",
            }
        ]
    if rendered:
        image_base = args.image_base.strip("/")
        visuals = []
        for item in rendered:
            page = item.get("page")
            filename = text(item.get("file"))
            src = f"{image_base}/{filename}" if image_base else filename
            visuals.append(
                {
                    "slide": f"Slide {page}",
                    "image": src,
                    "alt": f"Slide {page} course screenshot",
                    "title": f"Slide {page} memory title",
                    "what": "",
                    "how": "",
                    "remember": "",
                    "exam_sentence": "",
                    "dont_confuse": "",
                    "source": f"Course source: slide {page}.",
                }
            )
        spec["visuals"] = visuals
        spec["stats"] = [
            {"value": str(len(rendered)), "label": "selected slide images"},
            {"value": "fill", "label": "terms"},
            {"value": "fill", "label": "short answers"},
            {"value": "audit", "label": "quality gate"},
        ]

    write_json(Path(args.output), spec)
    print(f"Wrote spec scaffold: {args.output}")


def render_stat_cards(spec: dict[str, Any]) -> str:
    stats = as_list(spec.get("stats"))
    if not stats:
        stats = [
            {"value": len(as_list(spec.get("visuals"))), "label": "visual explanations"},
            {"value": len(as_list(spec.get("terms"))), "label": "terms"},
            {"value": len(as_list(spec.get("short_answers"))), "label": "short answers"},
            {"value": "HTML", "label": "fixed renderer"},
        ]
    parts = []
    for item in stats[:4]:
        if isinstance(item, dict):
            parts.append(f"<div class=\"stat\"><b>{esc(item.get('value'))}</b><span>{esc(item.get('label'))}</span></div>")
    return "\n".join(parts)


def render_source_summary(spec: dict[str, Any]) -> str:
    cards = []
    for item in as_list(spec.get("source_summary")):
        if not isinstance(item, dict):
            continue
        cards.append(
            "\n".join(
                [
                    "<article class=\"source-card\">",
                    f"  <span class=\"tag\">{esc(item.get('label', 'Source'))}</span>",
                    f"  <p><strong>{esc(item.get('text'))}</strong></p>",
                    f"  <p class=\"source-note\">{esc(item.get('source'))}</p>",
                    "</article>",
                ]
            )
        )
    return "\n".join(cards)


def render_module_dock(spec: dict[str, Any]) -> str:
    links = []
    for item in as_list(spec.get("module_nav")):
        if not isinstance(item, dict):
            continue
        cls = "module-current" if item.get("current") else ""
        sub = f"<span>{esc(item.get('sub'))}</span>" if text(item.get("sub")) else ""
        links.append(f"<a class=\"{cls}\" href=\"{esc(item.get('href'))}\">{esc(item.get('label'))}{sub}</a>")
    if not links:
        return ""
    return (
        "<div class=\"module-dock\" role=\"navigation\" aria-label=\"Course module switcher\">"
        "<details><summary><span>课程模块导航</span><span class=\"module-count\">"
        f"{len(links)} pages</span></summary><nav class=\"module-grid\">{''.join(links)}</nav></details></div>"
    )


def render_logic_map(spec: dict[str, Any]) -> str:
    cards = []
    for item in as_list(spec.get("logic_map")):
        if not isinstance(item, dict):
            continue
        cards.append(
            "\n".join(
                [
                    "<article class=\"logic-card\">",
                    f"  <span class=\"tag\">{esc(item.get('label'))}</span>",
                    f"  <h3>{esc(item.get('title'))}</h3>",
                    f"  <p>{esc(item.get('text'))}</p>",
                    f"  <p class=\"source-note\">{esc(item.get('source'))}</p>",
                    "</article>",
                ]
            )
        )
    return "\n".join(cards)


def render_visuals(spec: dict[str, Any]) -> str:
    cards = []
    for item in as_list(spec.get("visuals")):
        if not isinstance(item, dict):
            continue
        cards.append(
            "\n".join(
                [
                    "<figure class=\"visual-card\">",
                    f"  <img loading=\"lazy\" src=\"{esc(item.get('image'))}\" alt=\"{esc(item.get('alt', item.get('title')))}\">",
                    "  <figcaption>",
                    f"    <div class=\"tag\">{esc(item.get('slide', 'Slide'))}</div>",
                    f"    <b>{esc(item.get('title'))}</b>",
                    f"    <p class=\"lead\">{esc(item.get('what'))}</p>",
                    "    <div class=\"explain-list\">",
                    f"      <div class=\"explain-item\"><b>How to read / 怎么看</b><span>{esc(item.get('how'))}</span></div>",
                    f"      <div class=\"explain-item\"><b>Must remember / 必须记</b><span>{esc(item.get('remember'))}</span></div>",
                    f"      <div class=\"exam-line\">Exam sentence: {esc(item.get('exam_sentence'))}</div>",
                    f"      <div class=\"explain-item\"><b>Do not confuse / 别混淆</b><span>{esc(item.get('dont_confuse'))}</span></div>",
                    "    </div>",
                    f"    <p class=\"source-note\">{esc(item.get('source'))}</p>",
                    "  </figcaption>",
                    "</figure>",
                ]
            )
        )
    return "\n".join(cards)


def group_terms(terms: list[Any]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in terms:
        if not isinstance(item, dict):
            continue
        group = text(item.get("group")) or "Core terms"
        grouped.setdefault(group, []).append(item)
    return grouped


def render_terms(spec: dict[str, Any]) -> str:
    groups = []
    for group_name, items in group_terms(as_list(spec.get("terms"))).items():
        cards = []
        for item in items:
            cards.append(
                "\n".join(
                    [
                        f"<article class=\"term-card\" data-source=\"{esc(item.get('source'))}\">",
                        f"  <h4>{esc(item.get('term'))}</h4>",
                        f"  <p class=\"cn\">{esc(item.get('zh'))}</p>",
                        f"  <p class=\"en\">{esc(item.get('explanation_en'))}</p>",
                        f"  <p class=\"translation\">{esc(item.get('explanation_zh'))}</p>",
                        f"  <p class=\"source-note\">{esc(item.get('source'))}</p>",
                        "</article>",
                    ]
                )
            )
        groups.append(
            "\n".join(
                [
                    "<div class=\"term-group\">",
                    f"  <h3 class=\"group-title\"><span>{len(items)}</span>{esc(group_name)}</h3>",
                    f"  <div class=\"term-grid\">{''.join(cards)}</div>",
                    "</div>",
                ]
            )
        )
    return "\n".join(groups)


def render_short_answers(spec: dict[str, Any]) -> str:
    cards = []
    for item in as_list(spec.get("short_answers")):
        if not isinstance(item, dict):
            continue
        keywords = "".join(f"<span class=\"pill\">{esc(keyword)}</span>" for keyword in as_list(item.get("keywords")))
        cards.append(
            "\n".join(
                [
                    "<article class=\"answer-card\">",
                    f"  <h3>{esc(item.get('title'))}</h3>",
                    f"  <div class=\"model\">{esc(item.get('answer_en'))}</div>",
                    f"  <div class=\"translation\">{esc(item.get('answer_zh'))}</div>",
                    f"  <p class=\"source-note\">{esc(item.get('source'))}</p>",
                    f"  <div class=\"points\">{keywords}</div>",
                    "</article>",
                ]
            )
        )
    return "\n".join(cards)


def render_comparisons(spec: dict[str, Any]) -> str:
    blocks = []
    for item in as_list(spec.get("comparisons")):
        if not isinstance(item, dict):
            continue
        columns = [esc(col) for col in as_list(item.get("columns"))]
        rows = as_list(item.get("rows"))
        if not columns or not rows:
            continue
        header = "".join(f"<th>{col}</th>" for col in columns)
        body_rows = []
        for row in rows:
            if isinstance(row, list):
                cells = "".join(f"<td>{esc(cell)}</td>" for cell in row)
                body_rows.append(f"<tr>{cells}</tr>")
        blocks.append(
            "\n".join(
                [
                    "<article class=\"comparison-card\">",
                    f"  <h3>{esc(item.get('title', 'Comparison'))}</h3>",
                    "  <div class=\"table-wrap\">",
                    f"    <table><thead><tr>{header}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>",
                    "  </div>",
                    f"  <p class=\"source-note\">{esc(item.get('source'))}</p>",
                    "</article>",
                ]
            )
        )
    return "\n".join(blocks)


def render_confusions(spec: dict[str, Any]) -> str:
    cards = []
    for item in as_list(spec.get("confusions")):
        if not isinstance(item, dict):
            continue
        cards.append(
            "\n".join(
                [
                    "<article class=\"confusion-card\">",
                    f"  <h3>{esc(item.get('title'))}</h3>",
                    f"  <p><strong>Wrong shortcut:</strong> {esc(item.get('wrong'))}</p>",
                    f"  <p><strong>Exam-safe version:</strong> {esc(item.get('right'))}</p>",
                    f"  <p class=\"source-note\">{esc(item.get('source'))}</p>",
                    "</article>",
                ]
            )
        )
    return "\n".join(cards)


def render_review_order(spec: dict[str, Any]) -> str:
    cards = []
    for item in as_list(spec.get("review_order")):
        if not isinstance(item, dict):
            continue
        items = "".join(f"<li>{esc(point)}</li>" for point in as_list(item.get("items")))
        cards.append(
            "\n".join(
                [
                    "<article class=\"review-card\">",
                    f"  <h3>{esc(item.get('title'))}</h3>",
                    f"  <ul>{items}</ul>",
                    "</article>",
                ]
            )
        )
    return "\n".join(cards)


def render_html(spec: dict[str, Any]) -> str:
    section_links = [
        ("#logic", "结构"),
        ("#visuals", "图像"),
        ("#terms", "术语"),
        ("#answers", "短答"),
        ("#comparisons", "对比"),
        ("#confusions", "易混点"),
        ("#review", "背诵"),
    ]
    top_nav = "".join(f"<a href=\"{href}\">{label}</a>" for href, label in section_links)
    css = """
:root{--ink:#14202b;--muted:#647386;--paper:#f7f4ec;--panel:#fffdf7;--line:#d9d2c4;--teal:#006d77;--blue:#245f8f;--coral:#c94f2d;--green:#2f7d52;--amber:#9b6400;--teal-soft:#e4f4f1;--blue-soft:#e7eff8;--coral-soft:#fff0e8;--green-soft:#e8f4ed;--amber-soft:#fff5dc;--shadow:0 18px 42px rgba(42,36,24,.11);--font:Optima,"Avenir Next","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);font-family:var(--font);line-height:1.58;background:linear-gradient(120deg,#f7f4ec 0%,#e8f3f1 48%,#f7eee8 100%)}a{color:var(--teal)}.top{position:sticky;top:0;z-index:20;border-bottom:1px solid rgba(217,210,196,.85);background:rgba(247,244,236,.94);backdrop-filter:blur(16px)}.top-inner{max-width:1220px;margin:auto;padding:12px 18px;display:flex;gap:14px;align-items:center;justify-content:space-between}.brand{display:flex;gap:12px;align-items:center;min-width:0}.mark{width:42px;height:42px;border-radius:8px;background:conic-gradient(from 220deg,var(--teal),#8fc3bc,var(--coral),var(--blue),var(--teal));box-shadow:0 10px 26px rgba(20,32,43,.16);flex:0 0 auto}h1{font-size:22px;line-height:1.08;margin:0;letter-spacing:0}.subtitle{margin:2px 0 0;color:var(--muted);font-size:13px}.nav{display:flex;gap:8px;overflow:auto;max-width:61vw}.nav a{text-decoration:none;color:var(--teal);border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 10px;font-size:13px;white-space:nowrap}.wrap{max-width:1220px;margin:auto;padding:22px 18px 56px}.hero{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(320px,.95fr);gap:18px;align-items:stretch;margin-bottom:18px}.card,.hero-main,.hero-side,.band,.term-card,.answer-card,.logic-card,.source-card,.comparison-card,.confusion-card,.review-card{border:1px solid var(--line);background:rgba(255,253,247,.95);border-radius:8px;box-shadow:var(--shadow)}.hero-main{padding:24px;display:grid;align-content:center}.eyebrow{font-family:var(--mono);font-size:12px;color:var(--coral);text-transform:uppercase;font-weight:800;letter-spacing:.04em}.hero-main h2{font-size:44px;line-height:1.02;margin:8px 0 10px;letter-spacing:0}.hero-main p{font-size:18px;margin:0;color:#304353}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:18px}.stat{border:1px solid var(--line);border-radius:8px;padding:12px;background:#fff}.stat b{display:block;color:var(--teal);font-size:26px;line-height:1}.stat span{font-size:12px;color:var(--muted)}.hero-side{padding:18px}.source-grid{display:grid;gap:10px}.source-card{padding:13px;box-shadow:none}.tag{display:inline-flex;align-items:center;min-height:24px;padding:2px 8px;border-radius:999px;background:#e6f3ef;color:#0f5f59;font-size:.78rem;font-weight:800;white-space:nowrap}.band{padding:18px;margin:18px 0}.band h2,.section-title{font-size:28px;line-height:1.12;margin:0 0 10px;letter-spacing:0}.band p{color:#334b5a}.logic-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.logic-card{padding:14px}.logic-card h3{margin:8px 0 6px;font-size:20px}.visual-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-top:14px}.visual-card{border:1px solid var(--line);background:#fff;border-radius:8px;overflow:hidden;box-shadow:var(--shadow);margin:0}.visual-card img{display:block;width:100%;height:auto;background:#f3efe5}.visual-card figcaption{padding:12px 13px;border-top:1px solid var(--line)}.visual-card b{display:block;color:#17313a;margin-bottom:4px}.visual-card .lead{margin:6px 0 10px;color:#304353;font-size:15px}.explain-list{display:grid;gap:8px;margin-top:10px}.explain-item{border:1px solid #d8e6e3;background:#f3fbf9;border-radius:8px;padding:9px 10px}.explain-item b{font-family:var(--mono);font-size:11px;color:var(--teal);text-transform:uppercase;margin:0 0 3px}.explain-item span{font-size:14px;color:#314b56}.exam-line{border-left:4px solid var(--blue);background:var(--blue-soft);border-radius:8px;padding:9px 10px;margin-top:8px;color:#17324a}.term-groups{display:grid;gap:16px}.term-group{display:grid;gap:10px}.group-title{display:flex;align-items:center;gap:8px;margin:0;font-size:22px}.group-title span{font-family:var(--mono);font-size:12px;color:#fff;border-radius:999px;padding:3px 8px;background:var(--teal)}.term-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.term-card{padding:13px;position:relative;overflow:hidden}.term-card h4{font-size:19px;line-height:1.12;margin:0 0 5px}.cn{font-size:14px;color:#31414e;margin-bottom:7px}.en{border-left:4px solid var(--coral);background:var(--coral-soft);padding:8px 10px;border-radius:8px;color:#4e332b}.answers{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.answer-card{padding:16px}.answer-card h3{margin:0 0 8px;font-size:20px;color:#17313a}.model{background:var(--blue-soft);border-left:4px solid var(--blue);border-radius:8px;padding:12px;font-size:17px;color:#17324a}.translation{margin-top:9px;padding-top:9px;border-top:1px dashed rgba(36,95,143,.28);color:#40596a}.source-note{font-family:var(--mono);font-size:12px;color:var(--muted);margin-top:8px}.points{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}.pill{font-family:var(--mono);font-size:12px;color:#234150;border:1px solid #b9d6d2;background:#eef8f6;border-radius:999px;padding:4px 8px}.comparison-card,.confusion-card,.review-card{padding:16px;margin-top:12px}.table-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:8px;background:#fff}table{width:100%;border-collapse:collapse;min-width:720px}th,td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}th{background:#e7eee8;color:#263040;font-size:.9rem}.confusion-grid,.review-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.confusion-card{border-left:4px solid var(--amber)}.review-card{border-left:4px solid var(--green)}.review-card ul{margin:8px 0 0;padding-left:19px}.module-dock{position:fixed;right:14px;bottom:14px;z-index:2147482000;width:min(520px,calc(100vw - 28px));font-family:var(--font);color:#17212b}.module-dock details{border:1px solid rgba(43,68,73,.22);border-radius:8px;background:rgba(255,253,248,.97);box-shadow:0 16px 42px rgba(16,28,34,.18);overflow:hidden;backdrop-filter:blur(14px)}.module-dock summary{cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between;gap:10px;padding:10px 12px;font-size:14px;font-weight:800;color:#17343a}.module-dock summary::-webkit-details-marker{display:none}.module-count{font:700 11px/1 var(--mono);color:#66757c;border:1px solid rgba(43,68,73,.18);border-radius:999px;padding:4px 7px;background:#fff}.module-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;padding:0 10px 10px;max-height:min(58vh,430px);overflow:auto}.module-grid a{display:block;text-decoration:none;border:1px solid rgba(43,68,73,.18);border-radius:8px;background:#fff;color:#213d45;padding:8px 9px;font-size:13px;line-height:1.25;min-width:0;overflow-wrap:anywhere}.module-grid a:hover,.module-grid a.module-current{border-color:#006d77;background:#eef9f7;font-weight:800}.module-grid a span{display:block;margin-top:2px;font-size:11px;color:#66757c;font-weight:500}.en,.translation,.source-note,.source-card,.logic-card,.visual-card,.term-card,.answer-card{overflow-wrap:anywhere}@media(max-width:980px){.top-inner{display:block}.nav{max-width:none;margin-top:10px}.hero,.answers,.confusion-grid,.review-grid{grid-template-columns:1fr}.hero-main h2{font-size:34px}.stats{grid-template-columns:1fr 1fr}.visual-grid{grid-template-columns:1fr}.term-grid{grid-template-columns:1fr}.logic-grid{grid-template-columns:1fr}}@media(max-width:640px){.wrap{padding-left:12px;padding-right:12px}.nav{display:none}.module-dock{left:10px;right:10px;bottom:10px;width:auto}.module-grid{grid-template-columns:1fr;max-height:52vh}table{min-width:0;table-layout:fixed}th,td{padding:8px 7px;font-size:12px;line-height:1.35;overflow-wrap:anywhere;word-break:break-word}}@media print{.module-dock,.top{display:none!important}}
"""
    html_out = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(spec.get('module_title'))}</title>
<style>{css}</style>
</head>
<body>
{render_module_dock(spec)}
<header class="top">
  <div class="top-inner">
    <div class="brand"><div class="mark"></div><div><h1>{esc(spec.get('module_title'))}</h1><p class="subtitle">{esc(spec.get('module_subtitle'))}</p></div></div>
    <nav class="nav" aria-label="Page sections">{top_nav}</nav>
  </div>
</header>
<main class="wrap">
  <section class="hero">
    <div class="hero-main">
      <div class="eyebrow">{esc(spec.get('course_title'))}</div>
      <h2>{esc(spec.get('module_title'))}</h2>
      <p>{esc(spec.get('learner_profile'))}</p>
      <div class="stats">{render_stat_cards(spec)}</div>
    </div>
    <aside class="hero-side"><div class="source-grid">{render_source_summary(spec)}</div></aside>
  </section>
  <section id="logic" class="band"><h2>课件结构：先抓主线</h2><p>Use this section to reconstruct the lecture logic before memorizing details.</p><div class="logic-grid">{render_logic_map(spec)}</div></section>
  <section id="visuals" class="band"><h2>图像精讲：像读 PPT 一样理解每一页</h2><p>Every selected slide must explain what it teaches, how to read it, what to remember, one exam sentence, and one misconception.</p><div class="visual-grid">{render_visuals(spec)}</div></section>
  <section id="terms" class="band"><h2>术语卡：把英文专业词变成答题材料</h2><div class="term-groups">{render_terms(spec)}</div></section>
  <section id="answers" class="band"><h2>英文短答：可直接背诵和口试改写</h2><div class="answers">{render_short_answers(spec)}</div></section>
  <section id="comparisons" class="band"><h2>方法对比和分类表</h2>{render_comparisons(spec)}</section>
  <section id="confusions" class="band"><h2>易混点纠错</h2><div class="confusion-grid">{render_confusions(spec)}</div></section>
  <section id="review" class="band"><h2>背诵与自查顺序</h2><div class="review-grid">{render_review_order(spec)}</div></section>
</main>
</body>
</html>
"""
    return html_out


class MetricsParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.attrs: list[tuple[str, dict[str, str]]] = []
        self.text_parts: list[str] = []
        self.in_script_style = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        self.attrs.append((tag, {key: value or "" for key, value in attrs}))
        if tag in {"script", "style"}:
            self.in_script_style = True

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"}:
            self.in_script_style = False

    def handle_data(self, data: str) -> None:
        if not self.in_script_style:
            stripped = data.strip()
            if stripped:
                self.text_parts.append(stripped)


@dataclass
class HtmlMetrics:
    path: str
    bytes: int
    visible_text_chars: int
    chinese_chars: int
    english_words: int
    anchors: int
    navs: int
    tables: int
    figures: int
    images: int
    details: int
    term_cards: int
    answer_cards: int
    qa_cards: int
    explain_items: int
    exam_lines: int
    zh_blocks: int
    source_labels: int
    broken_images: list[str] = field(default_factory=list)
    placeholders: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "bytes": self.bytes,
            "visible_text_chars": self.visible_text_chars,
            "chinese_chars": self.chinese_chars,
            "english_words": self.english_words,
            "anchors": self.anchors,
            "navs": self.navs,
            "tables": self.tables,
            "figures": self.figures,
            "images": self.images,
            "details": self.details,
            "term_cards": self.term_cards,
            "answer_cards": self.answer_cards,
            "qa_cards": self.qa_cards,
            "explain_items": self.explain_items,
            "exam_lines": self.exam_lines,
            "zh_blocks": self.zh_blocks,
            "source_labels": self.source_labels,
            "broken_images": self.broken_images,
            "placeholders": self.placeholders,
        }


def class_tokens(parser: MetricsParser) -> list[str]:
    tokens: list[str] = []
    for _, attrs in parser.attrs:
        for item in attrs.get("class", "").split():
            tokens.append(item)
    return tokens


def resolve_image(html_path: Path, src: str) -> Path | None:
    if not src or src.startswith(("http://", "https://", "data:", "#")):
        return None
    if src.startswith("file://"):
        parsed = urlparse(src)
        return Path(unquote(parsed.path))
    return (html_path.parent / unquote(src)).resolve()


def collect_metrics(html_path: Path) -> HtmlMetrics:
    raw = html_path.read_text(encoding="utf-8", errors="ignore")
    parser = MetricsParser()
    parser.feed(raw)
    visible_text = " ".join(parser.text_parts)
    classes = class_tokens(parser)
    image_srcs = [attrs.get("src", "") for tag, attrs in parser.attrs if tag == "img"]
    broken = []
    for src in image_srcs:
        resolved = resolve_image(html_path, src)
        if resolved is not None and not resolved.exists():
            broken.append(src)
    placeholders = [pattern for pattern in PLACEHOLDER_PATTERNS if pattern.lower() in raw.lower()]
    return HtmlMetrics(
        path=str(html_path),
        bytes=html_path.stat().st_size,
        visible_text_chars=len(visible_text),
        chinese_chars=len(re.findall(r"[\u4e00-\u9fff]", visible_text)),
        english_words=len(re.findall(r"[A-Za-z][A-Za-z+/-]*", visible_text)),
        anchors=sum(1 for tag, _ in parser.attrs if tag == "a"),
        navs=sum(1 for tag, _ in parser.attrs if tag == "nav"),
        tables=sum(1 for tag, _ in parser.attrs if tag == "table"),
        figures=sum(1 for tag, _ in parser.attrs if tag == "figure"),
        images=len(image_srcs),
        details=sum(1 for tag, _ in parser.attrs if tag == "details"),
        term_cards=classes.count("term-card"),
        answer_cards=classes.count("answer-card"),
        qa_cards=classes.count("qa"),
        explain_items=classes.count("explain-item"),
        exam_lines=classes.count("exam-line"),
        zh_blocks=classes.count("zh") + classes.count("translation"),
        source_labels=classes.count("source") + classes.count("source-note"),
        broken_images=broken,
        placeholders=placeholders,
    )


def audit_metrics(metrics: HtmlMetrics, args: argparse.Namespace) -> list[str]:
    failures = []
    checks = [
        ("anchors", metrics.anchors, args.min_nav_links),
        ("navs", metrics.navs, 1 if args.require_nav else 0),
        ("figures", metrics.figures, args.min_visuals),
        ("images", metrics.images, args.min_visuals),
        ("term_cards", metrics.term_cards, args.min_terms),
        ("answer_cards", metrics.answer_cards, args.min_answers),
        ("explain_items", metrics.explain_items, args.min_explain_items),
        ("exam_lines", metrics.exam_lines, args.min_exam_lines),
        ("zh_blocks", metrics.zh_blocks, args.min_zh_blocks),
        ("source_labels", metrics.source_labels, args.min_source_labels),
    ]
    for name, actual, expected in checks:
        if actual < expected:
            failures.append(f"{name}={actual} < required {expected}")
    if args.require_chinese and metrics.chinese_chars < args.min_chinese_chars:
        failures.append(f"chinese_chars={metrics.chinese_chars} < required {args.min_chinese_chars}")
    if metrics.broken_images:
        failures.append(f"broken image paths: {', '.join(metrics.broken_images[:8])}")
    if metrics.placeholders:
        failures.append(f"placeholder text remains: {', '.join(metrics.placeholders)}")
    return failures


def command_render(args: argparse.Namespace) -> None:
    spec = load_json(Path(args.spec))
    errors = validate_spec(spec)
    if errors and not args.allow_invalid:
        for error in errors:
            print(f"SPEC ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_html(spec), encoding="utf-8")
    print(f"Wrote HTML: {out_path}")


def command_metrics(args: argparse.Namespace) -> None:
    metrics = collect_metrics(Path(args.html))
    print(json.dumps(metrics.as_dict(), indent=2, ensure_ascii=False))


def command_audit(args: argparse.Namespace) -> None:
    metrics = collect_metrics(Path(args.html))
    failures = audit_metrics(metrics, args)
    report = {"ok": not failures, "failures": failures, "metrics": metrics.as_dict()}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if failures:
        raise SystemExit(1)


def add_audit_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--min-nav-links", type=int, default=7)
    parser.add_argument("--min-visuals", type=int, default=6)
    parser.add_argument("--min-terms", type=int, default=20)
    parser.add_argument("--min-answers", type=int, default=10)
    parser.add_argument("--min-explain-items", type=int, default=18)
    parser.add_argument("--min-exam-lines", type=int, default=6)
    parser.add_argument("--min-zh-blocks", type=int, default=10)
    parser.add_argument("--min-source-labels", type=int, default=12)
    parser.add_argument("--min-chinese-chars", type=int, default=800)
    parser.add_argument("--require-nav", action="store_true", default=True)
    parser.add_argument("--no-require-nav", dest="require_nav", action="store_false")
    parser.add_argument("--require-chinese", action="store_true", default=True)
    parser.add_argument("--no-require-chinese", dest="require_chinese", action="store_false")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build or audit bilingual slide review HTML pages.")
    sub = parser.add_subparsers(dest="command", required=True)

    init_p = sub.add_parser("init-spec", help="Create a JSON content spec scaffold.")
    init_p.add_argument("--output", required=True)
    init_p.add_argument("--course-title", required=True)
    init_p.add_argument("--module-title", required=True)
    init_p.add_argument("--module-subtitle", default="Exam-oriented bilingual review page")
    init_p.add_argument("--manifest", help="Manifest from prepare_ppt_review_assets.py")
    init_p.add_argument("--image-base", default="", help="Relative prefix for images, e.g. assets/module")
    init_p.set_defaults(func=init_spec)

    render_p = sub.add_parser("render", help="Render fixed-layout HTML from a completed JSON spec.")
    render_p.add_argument("--spec", required=True)
    render_p.add_argument("--output", required=True)
    render_p.add_argument("--allow-invalid", action="store_true")
    render_p.set_defaults(func=command_render)

    metrics_p = sub.add_parser("metrics", help="Print structural metrics for an HTML page.")
    metrics_p.add_argument("--html", required=True)
    metrics_p.set_defaults(func=command_metrics)

    audit_p = sub.add_parser("audit", help="Fail if a review HTML page drifts below quality thresholds.")
    audit_p.add_argument("--html", required=True)
    add_audit_args(audit_p)
    audit_p.set_defaults(func=command_audit)

    validate_p = sub.add_parser("validate-spec", help="Validate a JSON spec before rendering.")
    validate_p.add_argument("--spec", required=True)
    validate_p.set_defaults(func=lambda args: validate_spec_command(args))
    return parser


def validate_spec_command(args: argparse.Namespace) -> None:
    errors = validate_spec(load_json(Path(args.spec)))
    print(json.dumps({"ok": not errors, "errors": errors}, indent=2, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
