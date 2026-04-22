"""HTML infographic renderers for WeChat-compatible output.

Each render function takes a parsed JSON block and returns an HTML string
using inline styles and <table> layout only — the safe subset that survives
the WeChat public-account editor's HTML sanitizer.

Supported block types:

- comparison: 2 or 3 side-by-side cards
- pyramid:    multi-tier cards (meant for hierarchical taxonomies)
- flowchart:  N horizontal nodes connected by arrows
- nested:     concentric boxes (for structural/hierarchical metaphors)

All blocks share a small color palette so different infographics in the
same article feel visually coherent.
"""
from __future__ import annotations

import html
import json
from typing import Any

PALETTES: dict[str, dict[str, str]] = {
    "blue":   {"main": "#2563EB", "bg": "#EFF6FF", "text_strong": "#1E40AF", "border": "#BFDBFE"},
    "orange": {"main": "#F97316", "bg": "#FFF7ED", "text_strong": "#9A3412", "border": "#FED7AA"},
    "green":  {"main": "#10B981", "bg": "#ECFDF5", "text_strong": "#065F46", "border": "#A7F3D0"},
    "amber":  {"main": "#F59E0B", "bg": "#FFFBEB", "text_strong": "#92400E", "border": "#FDE68A"},
    "purple": {"main": "#8B5CF6", "bg": "#F5F3FF", "text_strong": "#5B21B6", "border": "#DDD6FE"},
    "rose":   {"main": "#E11D48", "bg": "#FFF1F2", "text_strong": "#9F1239", "border": "#FECDD3"},
    "slate":  {"main": "#64748B", "bg": "#F8FAFC", "text_strong": "#334155", "border": "#CBD5E1"},
}


def esc(s: Any) -> str:
    """HTML-escape a value, turning None into empty string."""
    if s is None:
        return ""
    return html.escape(str(s), quote=False)


def palette(name: str | None) -> dict[str, str]:
    """Look up palette; fall back to blue for unknown/missing names."""
    return PALETTES.get((name or "blue").lower(), PALETTES["blue"])


def _title_block(title: str | None, subtitle: str | None) -> str:
    parts: list[str] = []
    if title:
        parts.append(
            f'<p style="text-align: center; font-size: 16px; font-weight: 600; color: #1F2937; margin: 0 0 6px;">{esc(title)}</p>'
        )
    if subtitle:
        parts.append(
            f'<p style="text-align: center; font-size: 13px; color: #6B7280; margin: 0 0 20px;">{esc(subtitle)}</p>'
        )
    return "".join(parts)


def _footnote(text: str | None) -> str:
    if not text:
        return ""
    return (
        f'<p style="text-align: center; font-size: 12px; color: #9CA3AF; '
        f'margin: 16px 0 0; font-style: italic;">{esc(text)}</p>'
    )


def render_comparison(data: dict) -> str:
    """Side-by-side cards. 2 or 3 columns.

    Schema:
        {
          "title": "...",
          "subtitle": "...",
          "columns": [
            {"label": "...", "content": "...", "note": "...", "color": "blue"},
            ...
          ],
          "footnote": "..."
        }
    """
    columns = data.get("columns", [])
    if not (2 <= len(columns) <= 3):
        raise ValueError("comparison requires 2 or 3 columns")
    col_pct = 100 // len(columns)

    cells: list[str] = []
    for col in columns:
        p = palette(col.get("color"))
        label = esc(col.get("label", ""))
        content = esc(col.get("content", ""))
        note = esc(col.get("note", ""))
        cells.append(
            f'<td style="width: {col_pct}%; background: {p["bg"]}; '
            f'border-radius: 12px; padding: 24px 20px; vertical-align: top; '
            f'border: 1px solid {p["border"]};">'
            + (
                f'<div style="display: inline-block; background: {p["main"]}; color: white; '
                f'font-size: 12px; font-weight: 600; padding: 4px 12px; border-radius: 4px; '
                f'margin-bottom: 16px;">{label}</div>'
                if label else ""
            )
            + (
                f'<div style="font-size: 16px; font-weight: 600; color: #1F2937; '
                f'line-height: 1.7; margin: 12px 0;">{content}</div>'
                if content else ""
            )
            + (
                f'<div style="font-size: 12px; color: #6B7280; margin-top: 12px;">{note}</div>'
                if note else ""
            )
            + "</td>"
        )

    table = (
        '<table style="width: 100%; border-collapse: separate; '
        'border-spacing: 12px 0;" cellpadding="0" cellspacing="0">'
        f'<tr>{"".join(cells)}</tr></table>'
    )

    return (
        '<section style="margin: 36px 0;">'
        + _title_block(data.get("title"), data.get("subtitle"))
        + table
        + _footnote(data.get("footnote"))
        + "</section>"
    )


def render_pyramid(data: dict) -> str:
    """Horizontal tiered cards, growing in strength/saturation left-to-right.

    Schema:
        {
          "title": "...",
          "subtitle": "...",
          "levels": [
            {"label": "...", "content": "...", "tag": "...", "color": "green"},
            ...
          ],
          "footnote": "..."
        }
    """
    levels = data.get("levels", [])
    if not levels:
        raise ValueError("pyramid requires at least one level")
    col_pct = 100 // len(levels)

    cells: list[str] = []
    for level in levels:
        p = palette(level.get("color"))
        label = esc(level.get("label", ""))
        content = esc(level.get("content", ""))
        tag = esc(level.get("tag", ""))
        cells.append(
            f'<td style="width: {col_pct}%; background: {p["bg"]}; '
            f'border-radius: 12px; padding: 22px 16px; vertical-align: top; '
            f'border-top: 4px solid {p["main"]};">'
            + (
                f'<div style="font-size: 15px; font-weight: 700; '
                f'color: {p["text_strong"]}; margin-bottom: 12px;">{label}</div>'
                if label else ""
            )
            + (
                f'<div style="font-size: 14px; color: #1F2937; line-height: 1.7; '
                f'font-style: italic; margin: 12px 0;">{content}</div>'
                if content else ""
            )
            + (
                f'<div style="margin-top: 16px; padding-top: 12px; '
                f'border-top: 1px solid {p["border"]}; font-size: 12px; '
                f'color: {p["main"]}; font-weight: 600;">{tag}</div>'
                if tag else ""
            )
            + "</td>"
        )

    table = (
        '<table style="width: 100%; border-collapse: separate; '
        'border-spacing: 10px 0;" cellpadding="0" cellspacing="0">'
        f'<tr>{"".join(cells)}</tr></table>'
    )

    return (
        '<section style="margin: 36px 0;">'
        + _title_block(data.get("title"), data.get("subtitle"))
        + table
        + _footnote(data.get("footnote"))
        + "</section>"
    )


def render_flowchart(data: dict) -> str:
    """Horizontal N-node flow with arrows between each node.

    Schema:
        {
          "title": "...",
          "subtitle": "...",
          "nodes": [
            {"label": "...", "content": "...", "note": "...", "color": "blue"},
            ...
          ],
          "footnote": "..."
        }
    """
    nodes = data.get("nodes", [])
    if len(nodes) < 2:
        raise ValueError("flowchart requires at least 2 nodes")

    arrow_count = len(nodes) - 1
    arrow_pct = 2.5
    node_pct = (100 - arrow_pct * arrow_count) / len(nodes)

    cells: list[str] = []
    for idx, node in enumerate(nodes):
        p = palette(node.get("color"))
        label = esc(node.get("label", ""))
        content_raw = node.get("content", "")
        note = esc(node.get("note", ""))
        # Preserve newlines in content by converting to <br>
        content_html = esc(content_raw).replace("\n", "<br>") if content_raw else ""

        cells.append(
            f'<td style="width: {node_pct:.2f}%; background: {p["bg"]}; '
            f'border-radius: 10px; padding: 16px 12px; vertical-align: top; '
            f'border-top: 3px solid {p["main"]};">'
            + (
                f'<div style="font-size: 13px; font-weight: 700; '
                f'color: {p["text_strong"]}; margin-bottom: 10px;">{label}</div>'
                if label else ""
            )
            + (
                f'<div style="font-size: 12px; color: #1F2937; line-height: 1.6; '
                f'margin: 10px 0;">{content_html}</div>'
                if content_html else ""
            )
            + (
                f'<div style="font-size: 11px; color: #4B5563; line-height: 1.5; '
                f'margin-top: 10px;">{note}</div>'
                if note else ""
            )
            + "</td>"
        )
        if idx < len(nodes) - 1:
            cells.append(
                f'<td style="width: {arrow_pct}%; text-align: center; '
                f'font-size: 18px; color: #9CA3AF; font-weight: bold;">→</td>'
            )

    table = (
        '<table style="width: 100%; border-collapse: separate; '
        'border-spacing: 0;" cellpadding="0" cellspacing="0">'
        f'<tr>{"".join(cells)}</tr></table>'
    )

    return (
        '<section style="margin: 36px 0;">'
        + _title_block(data.get("title"), data.get("subtitle"))
        + table
        + _footnote(data.get("footnote"))
        + "</section>"
    )


def render_nested(data: dict) -> str:
    """Concentric nested boxes — for structural/recursive metaphors.

    Schema:
        {
          "title": "...",
          "subtitle": "...",
          "layers": [
            {"text": "...", "color": "blue"},
            ...
          ],
          "footnote": "..."
        }

    Layers are rendered outermost-first.
    """
    layers = data.get("layers", [])
    if not layers:
        raise ValueError("nested requires at least one layer")

    def build(idx: int) -> str:
        if idx >= len(layers):
            return ""
        layer = layers[idx]
        p = palette(layer.get("color"))
        text = esc(layer.get("text", ""))
        radius = max(6, 12 - idx * 2)
        padding = max(12, 20 - idx * 2)
        inner = build(idx + 1)
        inner_block = f'<div style="margin-top: 10px;">{inner}</div>' if inner else ""
        return (
            f'<div style="background: {p["main"]}; border-radius: {radius}px; '
            f'padding: {padding}px; color: white;">'
            f'<div style="font-size: 12px; font-weight: 600; letter-spacing: 0.5px;">{text}</div>'
            f'{inner_block}</div>'
        )

    body = build(0)
    return (
        '<section style="margin: 36px 0;">'
        + _title_block(data.get("title"), data.get("subtitle"))
        + f'<div style="max-width: 480px; margin: 0 auto;">{body}</div>'
        + _footnote(data.get("footnote"))
        + "</section>"
    )


RENDERERS = {
    "comparison": render_comparison,
    "pyramid": render_pyramid,
    "flowchart": render_flowchart,
    "nested": render_nested,
}


def render_block(block_type: str, raw_json: str) -> str:
    """Parse a JSON block body and dispatch to the matching renderer.

    Returns a styled fallback HTML if the block type is unknown or the
    JSON is malformed — never raises to the caller, so a bad block does
    not abort the whole article render.
    """
    renderer = RENDERERS.get(block_type.lower())
    if renderer is None:
        return _error_card(f"unknown block type: {block_type}", raw_json)
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        return _error_card(f"invalid JSON in :::{block_type} — {e}", raw_json)
    try:
        return renderer(data)
    except Exception as e:
        return _error_card(f"error rendering :::{block_type} — {e}", raw_json)


def _error_card(msg: str, raw: str) -> str:
    return (
        '<section style="margin: 20px 0; padding: 16px; border: 2px dashed #E11D48; '
        'border-radius: 8px; background: #FFF1F2;">'
        f'<p style="margin: 0 0 8px; color: #9F1239; font-weight: 600;">⚠ {esc(msg)}</p>'
        f'<pre style="margin: 0; padding: 12px; background: white; border-radius: 4px; '
        f'font-family: monospace; font-size: 12px; color: #1F2937; overflow-x: auto; '
        f'white-space: pre-wrap;">{esc(raw)}</pre>'
        "</section>"
    )
