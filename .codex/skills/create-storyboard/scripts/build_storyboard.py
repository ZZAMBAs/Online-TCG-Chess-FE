#!/usr/bin/env python3
"""Build docs/design/storyboard.html from manifest, CSS, and page fragments."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path.cwd()
DESIGN_DIR = ROOT / "docs" / "design"
DEFAULT_MANIFEST = DESIGN_DIR / "storyboard-manifest.json"
DEFAULT_OUTPUT = DESIGN_DIR / "storyboard.html"
STORYBOARD_DIR = DESIGN_DIR / "storyboard"
STYLE_DIR = STORYBOARD_DIR / "styles"
FRAGMENT_DIR = STORYBOARD_DIR / "fragments"
FORBIDDEN_PATTERN = re.compile(r"<\s*iframe\b|srcdoc\s*=", re.IGNORECASE)
FRAGMENT_STYLE_PATTERN = re.compile(
    r"<\s*style\b|\sstyle\s*=",
    re.IGNORECASE,
)
PAGE_SCOPED_CSS_PATTERN = re.compile(
    r"(?:#page-|\.page-fragment--[a-z0-9-]+\s)",
    re.IGNORECASE,
)
REVIEW_STATUSES = {
    "draft",
    "needs-review",
    "approved",
    "needs-revision",
    "rejected",
    "blocked",
}
WORKFLOW_STAGES = {
    "structure-draft",
    "structure-review",
    "design-draft",
    "visual-review",
    "approved",
}


BASE_CSS = """
:root {
  --story-bg: #f6f7f9;
  --story-surface: #ffffff;
  --story-surface-muted: #eef2f6;
  --story-border: #d8dee7;
  --story-text: #16202a;
  --story-muted: #5c6978;
  --story-accent: #1f7a5c;
  --story-warning: #9a5b12;
  --story-danger: #b42318;
  --story-radius: 8px;
  --story-gap: 16px;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--story-bg);
  color: var(--story-text);
  line-height: 1.5;
}
a { color: inherit; }
.story-shell { max-width: 1440px; margin: 0 auto; padding: 32px 24px 64px; }
.story-header, .story-section {
  background: var(--story-surface);
  border: 1px solid var(--story-border);
  border-radius: var(--story-radius);
  padding: 20px;
  margin-bottom: 18px;
}
.story-header h1 { margin: 0 0 8px; font-size: 28px; }
.story-header p, .story-section p { color: var(--story-muted); }
.story-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: var(--story-gap); }
.story-list { margin: 0; padding-left: 20px; }
.story-pill {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 4px 10px;
  border: 1px solid var(--story-border);
  border-radius: 999px;
  background: var(--story-surface-muted);
  color: var(--story-muted);
  font-size: 13px;
}
.story-page {
  background: var(--story-surface);
  border: 1px solid var(--story-border);
  border-radius: var(--story-radius);
  margin: 24px 0;
  overflow: hidden;
}
.story-page__header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 18px 20px;
  border-bottom: 1px solid var(--story-border);
  background: #fafbfc;
}
.story-page__header h2 { margin: 0; font-size: 22px; }
.story-page__body { padding: 20px; }
.story-status-approved { border-color: var(--story-accent); color: var(--story-accent); }
.story-status-needs-revision, .story-status-rejected, .story-status-blocked { border-color: var(--story-danger); color: var(--story-danger); }
.story-status-draft, .story-status-needs-review { border-color: var(--story-warning); color: var(--story-warning); }
.story-review { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 6px; }
@media (max-width: 720px) {
  .story-shell { padding: 18px 12px 40px; }
  .story-header, .story-section, .story-page__body { padding: 14px; }
  .story-page__header { flex-direction: column; padding: 14px; }
}
""".strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        fail(f"Manifest not found: {path}")
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        fail(f"Invalid manifest JSON: {exc}")
    if not isinstance(data, dict):
        fail("Manifest root must be an object")
    return data


def page_items(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    pages = manifest.get("pages", [])
    if not isinstance(pages, list):
        fail("Manifest field 'pages' must be a list")
    result: list[dict[str, Any]] = []
    for index, page in enumerate(pages):
        if not isinstance(page, dict):
            fail(f"Page at index {index} must be an object")
        page_id = page.get("id")
        if not isinstance(page_id, str) or not page_id.strip():
            fail(f"Page at index {index} is missing a non-empty id")
        result.append(page)
    return result


def validate_workflow_state(
    manifest: dict[str, Any], pages: list[dict[str, Any]]
) -> None:
    if manifest.get("version") != 2:
        return
    stage = manifest.get("workflow_stage")
    if stage not in WORKFLOW_STAGES:
        fail(f"Invalid workflow_stage for manifest version 2: {stage}")
    statuses = [review_status(page) for page in pages]
    for page, (structure, visual) in zip(pages, statuses, strict=True):
        if structure not in REVIEW_STATUSES or visual not in REVIEW_STATUSES:
            fail(
                f"Invalid review status for page '{page['id']}': "
                f"structure={structure}, visual={visual}"
            )
    all_structure_approved = all(item[0] == "approved" for item in statuses)
    all_visual_approved = all(item[1] == "approved" for item in statuses)
    design = manifest.get("design") if isinstance(manifest.get("design"), dict) else {}
    baseline_status = str(design.get("baseline_status") or "blocked")
    if stage in {"design-draft", "visual-review", "approved"} and not all_structure_approved:
        fail(f"workflow_stage '{stage}' requires every structure review to be approved")
    if stage == "visual-review" and baseline_status not in {"draft", "needs-review"}:
        fail("visual-review requires a draft or needs-review design baseline")
    if stage == "approved" and (
        not all_visual_approved or baseline_status != "approved"
    ):
        fail("approved stage requires every visual review and design baseline to be approved")


def reject_forbidden(label: str, content: str) -> None:
    if FORBIDDEN_PATTERN.search(content):
        fail(f"Forbidden iframe/srcdoc usage found in {label}")


def reject_fragment_style(label: str, content: str) -> None:
    if FRAGMENT_STYLE_PATTERN.search(content):
        fail(f"Forbidden fragment-local style found in {label}")


def reject_page_scoped_css(label: str, content: str) -> None:
    if PAGE_SCOPED_CSS_PATTERN.search(content):
        fail(f"Forbidden page-scoped CSS found in {label}")


def list_values(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def render_list(items: list[str]) -> str:
    if not items:
        return "<p>기록된 항목이 없습니다.</p>"
    rows = "\n".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f'<ul class="story-list">\n{rows}\n</ul>'


def render_index(pages: list[dict[str, Any]]) -> str:
    links = []
    for page in pages:
        page_id = str(page["id"])
        title = str(page.get("title") or page_id)
        structure, visual = review_status(page)
        links.append(
            '<li>'
            f'<a href="#page-{html.escape(page_id)}">{html.escape(title)}</a> '
            f'<span class="story-pill story-status-{html.escape(structure)}">구조 {html.escape(structure)}</span> '
            f'<span class="story-pill story-status-{html.escape(visual)}">시각 {html.escape(visual)}</span>'
            '</li>'
        )
    return '<ul class="story-list">\n' + "\n".join(links) + "\n</ul>"


def css_bundle() -> str:
    chunks = [BASE_CSS]
    if STYLE_DIR.exists():
        for path in sorted(STYLE_DIR.glob("*.css")):
            content = read_text(path)
            reject_forbidden(str(path), content)
            reject_page_scoped_css(str(path), content)
            chunks.append(f"/* {path.relative_to(DESIGN_DIR)} */\n{content.strip()}")
    return "\n\n".join(chunks)


def fragment_path(page: dict[str, Any]) -> Path:
    raw_path = page.get("fragment")
    if isinstance(raw_path, str) and raw_path.strip():
        return DESIGN_DIR / raw_path
    return FRAGMENT_DIR / f"{page['id']}.html"


def review_status(page: dict[str, Any]) -> tuple[str, str]:
    review = page.get("review")
    if isinstance(review, dict):
        structure = str(review.get("structure") or "draft")
        visual = str(review.get("visual") or "blocked")
        return structure, visual
    legacy = str(page.get("status") or "draft")
    return legacy, "blocked"


def render_page(page: dict[str, Any]) -> str:
    page_id = str(page["id"])
    title = str(page.get("title") or page_id)
    structure, visual = review_status(page)
    path = fragment_path(page)
    if not path.exists():
        fail(f"Fragment not found for page '{page_id}': {path}")
    fragment = read_text(path).strip()
    reject_forbidden(str(path), fragment)
    reject_fragment_style(str(path), fragment)
    requirements = ", ".join(list_values(page.get("requirements"))) or "requirements pending"
    return f"""
<section class="story-page" id="page-{html.escape(page_id)}" data-page-id="{html.escape(page_id)}">
  <header class="story-page__header">
    <div>
      <h2>{html.escape(title)}</h2>
      <p>{html.escape(requirements)}</p>
    </div>
    <div class="story-review" aria-label="페이지 승인 상태">
      <span class="story-pill story-status-{html.escape(structure)}">구조 {html.escape(structure)}</span>
      <span class="story-pill story-status-{html.escape(visual)}">시각 {html.escape(visual)}</span>
    </div>
  </header>
  <div class="story-page__body">
{fragment}
  </div>
</section>
""".strip()


def render_document(manifest: dict[str, Any], pages: list[dict[str, Any]]) -> str:
    spec = manifest.get("spec") if isinstance(manifest.get("spec"), dict) else {}
    title = str(manifest.get("title") or "Online TCG Chess Storyboard")
    spec_bits = [
        f"BE commit: {spec.get('be_commit')}" if spec.get("be_commit") else "",
        f"sha256: {spec.get('sha256')}" if spec.get("sha256") else "",
        f"checked_at: {spec.get('checked_at')}" if spec.get("checked_at") else "",
    ]
    spec_text = " / ".join(bit for bit in spec_bits if bit) or "BE spec check metadata pending"
    workflow_stage = str(manifest.get("workflow_stage") or "legacy")
    design = manifest.get("design") if isinstance(manifest.get("design"), dict) else {}
    baseline_status = str(design.get("baseline_status") or "blocked")
    page_sections = "\n\n".join(render_page(page) for page in pages)
    return f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
{css_bundle()}
  </style>
</head>
<body>
  <main class="story-shell">
    <header class="story-header">
      <h1>{html.escape(title)}</h1>
      <p>{html.escape(spec_text)}</p>
      <p>workflow: {html.escape(workflow_stage)} / design baseline: {html.escape(baseline_status)}</p>
    </header>
    <section class="story-section" aria-labelledby="story-reading-guide">
      <h2 id="story-reading-guide">읽는 법</h2>
      <div class="story-grid">
        <p><strong>actual-ui</strong>: 구조 또는 시각 검토 중인 사용자 화면입니다.</p>
        <p><strong>story-note</strong>: 구현 판단을 위한 화면 밖 주석입니다.</p>
        <p><strong>dev-state</strong>: FE 상태명이나 서버 이벤트 상태입니다.</p>
      </div>
    </section>
    <section class="story-section" aria-labelledby="story-flow-summary">
      <h2 id="story-flow-summary">화면 흐름 요약</h2>
      {render_list(list_values(manifest.get("flow_summary")))}
    </section>
    <section class="story-section" aria-labelledby="story-handoff">
      <h2 id="story-handoff">구현 핸드오프</h2>
      {render_list(list_values(manifest.get("handoff")))}
    </section>
    <section class="story-section" aria-labelledby="story-index">
      <h2 id="story-index">페이지 목록</h2>
      {render_index(pages)}
    </section>
{page_sections}
  </main>
</body>
</html>
"""


def main() -> int:
    args = parse_args()
    manifest = load_manifest(args.manifest)
    pages = page_items(manifest)
    if not pages:
        fail("Manifest contains no pages")
    validate_workflow_state(manifest, pages)
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    document = render_document(manifest, pages)
    reject_forbidden("rendered document", document)
    output.write_text(document, encoding="utf-8")
    print(f"[OK] Built {output} with {len(pages)} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
