#!/usr/bin/env python3
"""Run multi-role review on an article.

Spawns 5 independent claude -p processes in parallel, each with a different
role prompt from roles/. Collects all reviews and generates a consolidated
summary.

Usage:
    python -m scripts.run_review <article-path> [--output-dir DIR] [--roles reader,editor,...]

Example:
    cd /path/to/writer-skill
    python -m scripts.run_review /path/to/article.md --output-dir /tmp/reviews
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from scripts.utils import get_roles_dir, make_claude_env

# Roles whose output is "builder" (modifies the article) rather than
# "reviewer" (produces feedback). They live in roles/ alongside reviewers
# for packaging convenience, but multi-role review excludes them — running
# a builder in a parallel review would overwrite the article.
BUILDER_ROLES: set[str] = {"info-architect"}


def discover_reviewer_roles() -> list[str]:
    """Scan roles/*.md and return reviewer role names, alphabetically sorted.

    Builder roles (see BUILDER_ROLES) are excluded. This lets us add new
    reviewer roles by dropping a file into roles/ without editing this script.
    """
    roles_dir = get_roles_dir()
    names = [p.stem for p in roles_dir.glob("*.md")]
    return sorted(n for n in names if n not in BUILDER_ROLES)


# Populated at import time so downstream code keeps working as before.
ALL_ROLES = discover_reviewer_roles()


def run_single_role(
    role_name: str,
    role_prompt: str,
    article_text: str,
    output_path: str,
    model: str | None = None,
) -> dict:
    """Run a single role review via claude -p. Returns result dict."""
    full_prompt = (
        f"{role_prompt}\n\n"
        f"---\n\n"
        f"## 请审查以下文章：\n\n"
        f"{article_text}"
    )

    cmd = ["claude", "-p", full_prompt, "--output-format", "text"]
    if model:
        cmd.extend(["--model", model])

    env = make_claude_env()
    start = time.time()

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=300, env=env
        )
        duration = time.time() - start
        review_text = result.stdout.strip()

        # Save review to file
        Path(output_path).write_text(review_text)

        return {
            "role": role_name,
            "status": "ok",
            "duration_seconds": round(duration, 1),
            "output_path": output_path,
            "preview": review_text[:200] + "..." if len(review_text) > 200 else review_text,
        }
    except subprocess.TimeoutExpired:
        return {"role": role_name, "status": "timeout", "duration_seconds": 300}
    except Exception as e:
        return {"role": role_name, "status": "error", "error": str(e)}


def generate_summary(output_dir: Path, results: list[dict]) -> str:
    """Read all review files and generate a consolidated markdown summary."""
    lines = [
        "# �� 多角色审查汇总报告\n",
        "## 审查状态\n",
        "| 角色 | 状态 | 耗时 |",
        "|---|---|---|",
    ]

    role_labels = {
        "reader": "读者",
        "editor": "编辑",
        "fact-checker": "事实核查",
        "style-coach": "文体教练",
        "strategist": "平台策略师",
    }

    for r in results:
        label = role_labels.get(r["role"], r["role"])
        status = "✅" if r["status"] == "ok" else "❌"
        duration = f'{r.get("duration_seconds", "?")}s'
        lines.append(f"| {label} | {status} | {duration} |")

    lines.append("\n---\n")
    lines.append("## 各角色完整报告\n")

    for r in results:
        if r["status"] == "ok":
            label = role_labels.get(r["role"], r["role"])
            filename = f"review-{r['role']}.md"
            lines.append(f"- [{label}审查]({filename})")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Run multi-role article review")
    parser.add_argument("article", type=Path, help="Path to article markdown file")
    parser.add_argument(
        "--output-dir", "-o", type=Path, default=None,
        help="Output directory for reviews (default: same dir as article)"
    )
    parser.add_argument(
        "--roles", type=str, default=None,
        help="Comma-separated list of roles to run (default: all 5)"
    )
    parser.add_argument("--model", type=str, default=None, help="Model override")
    parser.add_argument("--workers", type=int, default=5, help="Parallel workers")
    args = parser.parse_args()

    article_path = args.article.resolve()
    if not article_path.exists():
        print(f"Error: Article not found: {article_path}", file=sys.stderr)
        sys.exit(1)

    article_text = article_path.read_text()
    roles_dir = get_roles_dir()
    output_dir = (args.output_dir or article_path.parent).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine which roles to run
    role_names = args.roles.split(",") if args.roles else ALL_ROLES
    roles_to_run = []
    for name in role_names:
        name = name.strip()
        role_file = roles_dir / f"{name}.md"
        if not role_file.exists():
            print(f"Warning: Role file not found: {role_file}", file=sys.stderr)
            continue
        roles_to_run.append((name, role_file.read_text()))

    if not roles_to_run:
        print("Error: No valid roles to run", file=sys.stderr)
        sys.exit(1)

    print(f"Running {len(roles_to_run)} role reviews in parallel...")
    print(f"Article: {article_path}")
    print(f"Output:  {output_dir}\n")

    # Run all roles in parallel
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        future_to_role = {}
        for role_name, role_prompt in roles_to_run:
            out_path = str(output_dir / f"review-{role_name}.md")
            future = executor.submit(
                run_single_role, role_name, role_prompt, article_text, out_path, args.model
            )
            future_to_role[future] = role_name

        for future in as_completed(future_to_role):
            role_name = future_to_role[future]
            try:
                result = future.result()
            except Exception as e:
                result = {"role": role_name, "status": "error", "error": str(e)}
            results.append(result)
            status = "✅" if result["status"] == "ok" else "❌"
            print(f"  {status} {role_name} ({result.get('duration_seconds', '?')}s)")

    # Sort by original role order
    role_order = {name: i for i, (name, _) in enumerate(roles_to_run)}
    results.sort(key=lambda r: role_order.get(r["role"], 99))

    # Generate summary
    summary = generate_summary(output_dir, results)
    summary_path = output_dir / "consolidated-review.md"
    summary_path.write_text(summary)

    # Save metadata
    meta = {
        "article": str(article_path),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "results": results,
    }
    (output_dir / "review-metadata.json").write_text(json.dumps(meta, indent=2))

    print(f"\nDone. Summary: {summary_path}")
    ok_count = sum(1 for r in results if r["status"] == "ok")
    print(f"Results: {ok_count}/{len(results)} reviews completed successfully")


if __name__ == "__main__":
    main()
