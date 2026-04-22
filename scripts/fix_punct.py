#!/usr/bin/env python3
"""Fix half-width ASCII punctuation to full-width CJK punctuation in Chinese text.

Rule: replace ASCII ,.?!; with ，。?!; when adjacent to CJK characters.
Protects: code fences (```), infographic blocks (:::), URLs in [text](url),
decimal points between digits, inline code in backticks.

Usage:
    python3 -m scripts.fix_punct <file> [--dry-run]
    python3 -m scripts.fix_punct <file1> <file2> ...
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CJK_RANGES = [
    (0x4E00, 0x9FFF),   # CJK Unified Ideographs
    (0x3400, 0x4DBF),   # Extension A
    (0x3000, 0x303F),   # CJK Symbols
    (0xFF00, 0xFFEF),   # Halfwidth/Fullwidth Forms
]

PUNCT_MAP = {
    ",": "，",
    ".": "。",
    "?": "？",
    "!": "！",
    ";": "；",
    ":": "：",
}


def is_cjk(ch: str) -> bool:
    if not ch:
        return False
    cp = ord(ch)
    return any(lo <= cp <= hi for lo, hi in CJK_RANGES)


def fix_line(line: str) -> tuple[str, int]:
    """Fix punctuation in one line. Returns (new_line, replacement_count).

    Strategy: if a line's CJK ratio >= 30% (i.e. it's a Chinese sentence
    with some English words mixed in), replace ALL ASCII punctuation with
    full-width equivalents, except:
    - decimal points (digit.digit)
    - punctuation inside inline code (`...`)
    - punctuation inside markdown links [text](url)
    - English sentence terminators when the line is actually English-dominant
    """
    if not any(is_cjk(c) for c in line):
        return line, 0  # pure ASCII line, don't touch

    # Is this line a Chinese sentence? Count CJK ratio (exclude whitespace).
    non_space = [c for c in line if not c.isspace()]
    if non_space:
        cjk_count = sum(1 for c in non_space if is_cjk(c))
        cjk_ratio = cjk_count / len(non_space)
    else:
        cjk_ratio = 0
    chinese_sentence = cjk_ratio >= 0.3

    # Mask inline code `...` and markdown link URLs
    masks = []

    def stash(m):
        masks.append(m.group(0))
        return f"\x00{len(masks)-1}\x00"

    masked = re.sub(r"`[^`]+`", stash, line)
    masked = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", stash, masked)

    chars = list(masked)
    out = []
    count = 0
    for i, c in enumerate(chars):
        if c in PUNCT_MAP:
            prev = chars[i-1] if i > 0 else ""
            nxt = chars[i+1] if i < len(chars)-1 else ""

            # Protect decimal points: digit.digit
            if c == "." and prev.isdigit() and nxt.isdigit():
                out.append(c)
                continue

            if chinese_sentence:
                # Chinese-dominant line: replace the ASCII punct with CJK version
                out.append(PUNCT_MAP[c])
                count += 1
                continue
            else:
                # English-dominant line: only replace if immediately adjacent to CJK
                if is_cjk(prev) or is_cjk(nxt):
                    out.append(PUNCT_MAP[c])
                    count += 1
                    continue
        out.append(c)

    result = "".join(out)
    for i, m in enumerate(masks):
        result = result.replace(f"\x00{i}\x00", m)
    return result, count


def fix_file(path: Path, dry_run: bool = False) -> int:
    """Fix a markdown file in place. Returns total replacement count."""
    text = path.read_text()
    lines = text.split("\n")
    new_lines = []
    total = 0
    in_fence = False   # ``` code fence
    in_block = False   # ::: infographic block

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            new_lines.append(line)
            continue
        if stripped.startswith(":::"):
            in_block = not in_block
            new_lines.append(line)
            continue
        if in_fence or in_block:
            new_lines.append(line)  # don't touch code or block JSON
            continue
        fixed, n = fix_line(line)
        new_lines.append(fixed)
        total += n

    new_text = "\n".join(new_lines)
    if not dry_run and new_text != text:
        path.write_text(new_text)
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="show count without writing")
    args = parser.parse_args()

    for f in args.files:
        if not f.exists():
            print(f"skip (not found): {f}", file=sys.stderr)
            continue
        n = fix_file(f, dry_run=args.dry_run)
        action = "would fix" if args.dry_run else "fixed"
        print(f"{action} {n:4d} punct in {f}")


if __name__ == "__main__":
    main()
