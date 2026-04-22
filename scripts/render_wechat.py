#!/usr/bin/env python3
"""Render a markdown article to WeChat-compatible HTML.

WeChat's public-account editor strips class attributes and external CSS.
It only preserves inline style on a narrow set of tags. This script produces
a single self-contained HTML file where the article body uses inline style +
<table> layout (no flex/grid), safe to copy-paste into the editor.

The output page also includes a top toolbar with a one-click copy button
that selects only the article area — the toolbar itself is not copied.

Usage:
    python -m scripts.render_wechat <article.md> [--output FILE] [--open]

Example:
    python -m scripts.render_wechat examples/article-distill-your-ex.md --open
"""
from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from pathlib import Path

try:
    from scripts.infographics import render_block as render_infographic_block
except ImportError:  # allow `python scripts/render_wechat.py ...` direct run
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from scripts.infographics import render_block as render_infographic_block

ACCENT = "#2563EB"
ACCENT_DARK = "#1E40AF"
TEXT = "#1F2937"
MUTED = "#6B7280"
BORDER = "#E5E7EB"
CODE_BG = "#1F2937"
CODE_FG = "#F9FAFB"
INLINE_CODE_BG = "#F3F4F6"
INLINE_CODE_FG = "#DC2626"

PARA_STYLE = f"margin: 0 0 20px; line-height: 1.9; color: {TEXT}; font-size: 16px;"
H1_STYLE = f"font-size: 26px; font-weight: 700; color: {TEXT}; line-height: 1.4; margin: 0 0 32px; letter-spacing: 0.5px;"
H2_STYLE = f"font-size: 22px; font-weight: 700; color: {TEXT}; line-height: 1.4; margin: 40px 0 20px; padding-left: 14px; border-left: 4px solid {ACCENT};"
H3_STYLE = f"font-size: 18px; font-weight: 700; color: {TEXT}; line-height: 1.4; margin: 30px 0 16px;"
STRONG_STYLE = f"color: {ACCENT}; font-weight: 700;"
EM_STYLE = "font-style: italic;"
CODE_INLINE_STYLE = f"background: {INLINE_CODE_BG}; padding: 2px 6px; border-radius: 3px; font-family: 'SF Mono', Consolas, 'Courier New', monospace; font-size: 13px; color: {INLINE_CODE_FG};"
CODE_BLOCK_STYLE = f"background: {CODE_BG}; color: {CODE_FG}; padding: 20px; border-radius: 8px; font-family: 'SF Mono', Consolas, 'Courier New', monospace; font-size: 13px; line-height: 1.7; overflow-x: auto; margin: 20px 0;"
BLOCKQUOTE_STYLE = f"margin: 20px 0; padding: 12px 20px; border-left: 4px solid {ACCENT}; background: #F9FAFB; color: {MUTED}; font-style: italic;"
UL_STYLE = f"margin: 0 0 20px; padding-left: 24px; line-height: 1.9; color: {TEXT}; font-size: 16px;"
OL_STYLE = UL_STYLE
LI_STYLE = "margin: 0 0 8px;"
HR_STYLE = f"border: none; border-top: 1px solid {BORDER}; margin: 32px 0;"
IMG_STYLE = "max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 4px;"
LINK_STYLE = f"color: {ACCENT}; text-decoration: none; border-bottom: 1px solid {ACCENT};"


def render_inline(text: str) -> str:
    """Apply inline-level markdown rules: bold, italic, code, link."""
    text = html.escape(text, quote=False)

    placeholders: list[str] = []

    def stash(s: str) -> str:
        placeholders.append(s)
        return f"\x00{len(placeholders) - 1}\x00"

    # Inline code first — its content is not further processed
    text = re.sub(
        r"`([^`]+)`",
        lambda m: stash(f'<code style="{CODE_INLINE_STYLE}">{m.group(1)}</code>'),
        text,
    )
    # Links [text](url)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: stash(f'<a href="{m.group(2)}" style="{LINK_STYLE}">{m.group(1)}</a>'),
        text,
    )
    # Bold (** or __)
    text = re.sub(r"\*\*([^*]+)\*\*", rf'<strong style="{STRONG_STYLE}">\1</strong>', text)
    text = re.sub(r"__([^_]+)__", rf'<strong style="{STRONG_STYLE}">\1</strong>', text)
    # Italic (single * or _)
    text = re.sub(r"(?<![*])\*([^*\n]+)\*(?![*])", rf'<em style="{EM_STYLE}">\1</em>', text)
    text = re.sub(r"(?<![_])_([^_\n]+)_(?![_])", rf'<em style="{EM_STYLE}">\1</em>', text)

    for i, p in enumerate(placeholders):
        text = text.replace(f"\x00{i}\x00", p)
    return text


def render_body(md: str) -> str:
    """Convert markdown body to HTML with inline styles."""
    lines = md.split("\n")
    out: list[str] = []
    i = 0

    def flush_para(buf: list[str]):
        if not buf:
            return
        joined = " ".join(s.strip() for s in buf).strip()
        if joined:
            out.append(f'<p style="{PARA_STYLE}">{render_inline(joined)}</p>')

    para_buf: list[str] = []

    while i < len(lines):
        line = lines[i]

        # Infographic block: :::type ... :::
        info_match = re.match(r"^:::\s*([a-zA-Z][a-zA-Z0-9_-]*)\s*$", line)
        if info_match:
            flush_para(para_buf)
            para_buf = []
            block_type = info_match.group(1)
            i += 1
            body_lines: list[str] = []
            while i < len(lines) and not lines[i].startswith(":::"):
                body_lines.append(lines[i])
                i += 1
            i += 1  # skip closing :::
            out.append(render_infographic_block(block_type, "\n".join(body_lines)))
            continue

        # Fenced code block
        if line.startswith("```"):
            flush_para(para_buf)
            para_buf = []
            i += 1
            code_lines: list[str] = []
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            body = html.escape("\n".join(code_lines))
            out.append(f'<pre style="{CODE_BLOCK_STYLE}">{body}</pre>')
            continue

        # Headings
        m = re.match(r"^(#{1,3})\s+(.+)$", line)
        if m:
            flush_para(para_buf)
            para_buf = []
            level = len(m.group(1))
            content = render_inline(m.group(2).strip())
            style = {1: H1_STYLE, 2: H2_STYLE, 3: H3_STYLE}[level]
            out.append(f'<h{level} style="{style}">{content}</h{level}>')
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^(-{3,}|\*{3,}|_{3,})\s*$", line):
            flush_para(para_buf)
            para_buf = []
            out.append(f'<hr style="{HR_STYLE}">')
            i += 1
            continue

        # Blockquote
        if line.startswith("> "):
            flush_para(para_buf)
            para_buf = []
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].startswith("> "):
                quote_lines.append(lines[i][2:])
                i += 1
            content = render_inline(" ".join(s.strip() for s in quote_lines))
            out.append(f'<blockquote style="{BLOCKQUOTE_STYLE}">{content}</blockquote>')
            continue

        # Unordered list
        if re.match(r"^[-*+]\s+", line):
            flush_para(para_buf)
            para_buf = []
            items: list[str] = []
            while i < len(lines) and re.match(r"^[-*+]\s+", lines[i]):
                items.append(re.sub(r"^[-*+]\s+", "", lines[i]))
                i += 1
            li_html = "".join(f'<li style="{LI_STYLE}">{render_inline(it)}</li>' for it in items)
            out.append(f'<ul style="{UL_STYLE}">{li_html}</ul>')
            continue

        # Ordered list
        if re.match(r"^\d+\.\s+", line):
            flush_para(para_buf)
            para_buf = []
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i]))
                i += 1
            li_html = "".join(f'<li style="{LI_STYLE}">{render_inline(it)}</li>' for it in items)
            out.append(f'<ol style="{OL_STYLE}">{li_html}</ol>')
            continue

        # Standalone image on its own line: ![alt](src)
        img_match = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", line.strip())
        if img_match:
            flush_para(para_buf)
            para_buf = []
            alt = html.escape(img_match.group(1), quote=True)
            src = html.escape(img_match.group(2), quote=True)
            out.append(f'<img src="{src}" alt="{alt}" style="{IMG_STYLE}">')
            i += 1
            continue

        # Blank line flushes paragraph
        if line.strip() == "":
            flush_para(para_buf)
            para_buf = []
            i += 1
            continue

        # Accumulate into paragraph
        para_buf.append(line)
        i += 1

    flush_para(para_buf)
    return "\n\n".join(out)


def wrap_page(body_html: str, title: str) -> str:
    """Wrap article body in a preview page with a one-click copy toolbar."""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{html.escape(title)} · 微信预览</title>
<style>
  body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; background: #F5F5F5; }}
  .toolbar {{ position: sticky; top: 0; z-index: 100; background: #1F2937; color: white; padding: 14px 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
  .toolbar .hint {{ font-size: 13px; color: #D1D5DB; }}
  .toolbar button {{ background: #2563EB; color: white; border: none; padding: 8px 18px; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500; }}
  .toolbar button:hover {{ background: #1D4ED8; }}
  .toolbar button.copied {{ background: #10B981; }}
  .container {{ max-width: 720px; margin: 30px auto; background: white; padding: 48px 40px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
  .copy-boundary {{ border: 2px dashed #D1D5DB; padding: 20px; border-radius: 4px; }}
  @media print {{ .toolbar {{ display: none; }} .container {{ box-shadow: none; margin: 0; }} }}
</style>
</head>
<body>

<div class="toolbar">
  <span class="hint">选中虚线框内内容 → 复制 → 粘贴到微信公众号编辑器</span>
  <button id="copyBtn" onclick="copyContent()">一键复制正文</button>
</div>

<div class="container">
<div class="copy-boundary">

<section id="copyArea" style="font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif; color: {TEXT}; line-height: 1.8; font-size: 16px;">

{body_html}

</section>

</div>
</div>

<script>
function copyContent() {{
  const area = document.getElementById('copyArea');
  const range = document.createRange();
  range.selectNode(area);
  const sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  try {{
    document.execCommand('copy');
    sel.removeAllRanges();
    const btn = document.getElementById('copyBtn');
    const original = btn.textContent;
    btn.textContent = '✓ 已复制，去微信粘贴';
    btn.classList.add('copied');
    setTimeout(() => {{ btn.textContent = original; btn.classList.remove('copied'); }}, 2500);
  }} catch (e) {{
    alert('复制失败，请手动选中虚线框内容复制');
  }}
}}
</script>

</body>
</html>
"""


def render_file(md_path: Path, out_path: Path) -> Path:
    md = md_path.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else md_path.stem
    body = render_body(md)
    page = wrap_page(body, title)
    out_path.write_text(page, encoding="utf-8")
    return out_path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("article", type=Path, help="path to the markdown article")
    ap.add_argument("--output", "-o", type=Path, help="output HTML path (default: <article>.html)")
    ap.add_argument("--open", action="store_true", help="open the output in the default browser")
    args = ap.parse_args(argv)

    if not args.article.is_file():
        print(f"error: not a file: {args.article}", file=sys.stderr)
        return 1

    out_path = args.output or args.article.with_suffix(".html")
    render_file(args.article, out_path)
    print(f"wrote {out_path}")

    if args.open:
        if sys.platform == "darwin":
            subprocess.run(["open", str(out_path)])
        elif sys.platform == "win32":
            subprocess.run(["cmd", "/c", "start", "", str(out_path)], shell=False)
        else:
            subprocess.run(["xdg-open", str(out_path)])

    return 0


if __name__ == "__main__":
    sys.exit(main())
