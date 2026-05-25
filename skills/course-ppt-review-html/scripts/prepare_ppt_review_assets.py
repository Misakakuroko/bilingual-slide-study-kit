#!/usr/bin/env python3
"""Prepare slide text and screenshots for bilingual course review HTML pages."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise SystemExit(f"Required tool not found: {name}")
    return path


def parse_pages(spec: str) -> list[int]:
    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s), int(end_s)
            if end < start:
                raise SystemExit(f"Invalid page range: {part}")
            pages.update(range(start, end + 1))
        else:
            pages.add(int(part))
    if not pages:
        raise SystemExit("No pages selected")
    return sorted(pages)


def run(cmd: list[str]) -> str:
    completed = subprocess.run(cmd, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return completed.stdout


def pdf_page_count(pdfinfo: str, pdf: Path) -> int:
    info = run([pdfinfo, str(pdf)])
    for line in info.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise SystemExit("Could not determine PDF page count")


def write_visual_snippets(path: Path, rendered: list[dict]) -> None:
    lines = ["<div class=\"visual-grid\">"]
    for item in rendered:
        page = item["page"]
        image = item["file"]
        lines.extend(
            [
                "  <figure class=\"visual-card\">",
                f"    <img loading=\"lazy\" src=\"{image}\" alt=\"Slide {page} course screenshot\">",
                "    <figcaption>",
                f"      <div class=\"tag\">slide {page}</div>",
                "      <b>Add a memory title</b>",
                "      <p class=\"lead\">Explain what this PPT page is teaching.</p>",
                "      <div class=\"explain-list\">",
                "        <div class=\"explain-item\"><b>How to read</b><span>Explain how to read the figure/table.</span></div>",
                "        <div class=\"explain-item\"><b>Must remember</b><span>State the key concept.</span></div>",
                "        <div class=\"exam-line\">Exam sentence: Add a complete, exam-ready sentence.</div>",
                "        <div class=\"explain-item\"><b>Do not confuse</b><span>Add one common misconception.</span></div>",
                "      </div>",
                "    </figcaption>",
                "  </figure>",
            ]
        )
    lines.append("</div>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def clean_prefix_files(output_dir: Path, prefix: str) -> None:
    for existing in output_dir.glob(f"{prefix}*"):
        if existing.is_file():
            existing.unlink()
    for existing in output_dir.glob(f".{prefix}*"):
        if existing.is_file():
            existing.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract lecture slide text and screenshots for HTML review pages.")
    parser.add_argument("--pdf", required=True, help="Source lecture PDF")
    parser.add_argument("--output-dir", required=True, help="Directory for generated assets")
    parser.add_argument("--prefix", required=True, help="Output filename prefix, e.g. recording")
    parser.add_argument("--pages", required=True, help="Pages to render, e.g. 3,4,7-10,16")
    parser.add_argument("--dpi", type=int, default=150, help="Render DPI")
    parser.add_argument("--quality", type=int, default=82, help="JPEG quality for pdftoppm")
    parser.add_argument("--max-width", type=int, default=1280, help="Resize max width using sips when available")
    parser.add_argument("--clean", action="store_true", help="Delete old files with this prefix in output dir first")
    args = parser.parse_args()

    pdf = Path(args.pdf).expanduser().resolve()
    if not pdf.exists():
        raise SystemExit(f"PDF not found: {pdf}")

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    pdfinfo = require_tool("pdfinfo")
    pdftotext = require_tool("pdftotext")
    pdftoppm = require_tool("pdftoppm")
    sips = shutil.which("sips")

    pages = parse_pages(args.pages)
    total_pages = pdf_page_count(pdfinfo, pdf)
    invalid = [p for p in pages if p < 1 or p > total_pages]
    if invalid:
        raise SystemExit(f"Page(s) outside 1..{total_pages}: {invalid}")

    if args.clean:
        clean_prefix_files(output_dir, args.prefix)

    text_path = output_dir / f"{args.prefix}_slides_text.txt"
    run([pdftotext, "-layout", str(pdf), str(text_path)])

    rendered: list[dict] = []
    for page in pages:
        pad = f"{page:02d}"
        out_name = f"{args.prefix}-slide-{pad}.jpg"
        tmp_base = output_dir / f".{args.prefix}-slide-{pad}-tmp"
        tmp_jpg = tmp_base.with_suffix(".jpg")
        final_jpg = output_dir / out_name
        if tmp_jpg.exists():
            tmp_jpg.unlink()
        run(
            [
                pdftoppm,
                "-f",
                str(page),
                "-l",
                str(page),
                "-singlefile",
                "-jpeg",
                "-jpegopt",
                f"quality={args.quality}",
                "-r",
                str(args.dpi),
                str(pdf),
                str(tmp_base),
            ]
        )
        tmp_jpg.replace(final_jpg)
        if sips and args.max_width > 0:
            subprocess.run([sips, "-Z", str(args.max_width), str(final_jpg)], check=True, stdout=subprocess.DEVNULL)
        rendered.append({"page": page, "file": out_name, "bytes": final_jpg.stat().st_size})

    manifest_path = output_dir / f"{args.prefix}_manifest.json"
    snippet_path = output_dir / f"{args.prefix}_visual_snippets.html"
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_pdf": str(pdf),
        "total_pages": total_pages,
        "text_file": text_path.name,
        "prefix": args.prefix,
        "rendered": rendered,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_visual_snippets(snippet_path, rendered)
    print(
        json.dumps(
            {
                "text": str(text_path),
                "manifest": str(manifest_path),
                "snippets": str(snippet_path),
                "images": len(rendered),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
