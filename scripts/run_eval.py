#!/usr/bin/env python3
"""Run eval test cases for the writer skill.

Executes each test prompt from evals.json twice — once with the skill and once
without — saving outputs for comparison. Compatible with skill-creator's
generate_review.py viewer.

Usage:
    python -m scripts.run_eval --workspace /path/to/workspace [--evals evals/evals.json]

Output structure (skill-creator compatible):
    workspace/
    ├── eval-0/
    │   ├── eval_metadata.json
    │   ├── with_skill/
    │   │   ├── outputs/
    │   │   └── timing.json
    │   └── without_skill/
    │       ├── outputs/
    │       └── timing.json
    └── eval-1/
        └── ...
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

from scripts.utils import get_skill_dir, make_claude_env


def run_single_eval(
    prompt: str,
    output_dir: str,
    use_skill: bool,
    skill_path: str | None = None,
    model: str | None = None,
) -> dict:
    """Run a single eval via claude -p. Returns timing info."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Build prompt with instruction to save outputs
    full_prompt = (
        f"{prompt}\n\n"
        f"请把文章保存到 {output_dir}/article.md。"
        f"如果有事实核查结果，保存到 {output_dir}/review.md。"
        f"如果有平台格式版本，也保存到对应文件中。"
    )

    cmd = ["claude", "-p", full_prompt, "--output-format", "text"]
    if model:
        cmd.extend(["--model", model])
    if use_skill and skill_path:
        cmd.extend(["--allowedTools", f"Read({skill_path}/**)"])

    env = make_claude_env()
    start = time.time()

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=600, env=env
        )
        duration = time.time() - start

        # Save transcript
        transcript_path = Path(output_dir) / "transcript.md"
        transcript_path.write_text(
            f"## Eval Prompt\n\n{prompt}\n\n## Output\n\n{result.stdout}"
        )

        timing = {
            "duration_seconds": round(duration, 1),
            "use_skill": use_skill,
        }
        return timing

    except subprocess.TimeoutExpired:
        return {"duration_seconds": 600, "use_skill": use_skill, "error": "timeout"}
    except Exception as e:
        return {"duration_seconds": 0, "use_skill": use_skill, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Run writer skill evals")
    parser.add_argument("--workspace", "-w", type=Path, required=True, help="Workspace directory")
    parser.add_argument("--evals", "-e", type=Path, default=None, help="Path to evals.json")
    parser.add_argument("--model", type=str, default=None, help="Model override")
    parser.add_argument("--only", type=int, nargs="*", help="Only run specific eval IDs")
    parser.add_argument("--skip-baseline", action="store_true", help="Skip without_skill runs")
    args = parser.parse_args()

    skill_dir = get_skill_dir()
    evals_path = args.evals or (skill_dir / "evals" / "evals.json")

    if not evals_path.exists():
        print(f"Error: Evals file not found: {evals_path}", file=sys.stderr)
        sys.exit(1)

    evals_data = json.loads(evals_path.read_text())
    eval_cases = evals_data.get("evals", [])

    if args.only:
        eval_cases = [e for e in eval_cases if e["id"] in args.only]

    workspace = args.workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    print(f"Running {len(eval_cases)} eval(s)")
    print(f"Workspace: {workspace}")
    print(f"Skill: {skill_dir}\n")

    for case in eval_cases:
        eval_id = case["id"]
        prompt = case["prompt"]
        eval_dir = workspace / f"eval-{eval_id}"

        # Save metadata
        eval_dir.mkdir(parents=True, exist_ok=True)
        (eval_dir / "eval_metadata.json").write_text(json.dumps({
            "eval_id": eval_id,
            "prompt": prompt,
            "expected_output": case.get("expected_output", ""),
            "eval_name": f"Eval {eval_id}: {prompt[:50]}...",
        }, indent=2, ensure_ascii=False))

        # Run with_skill
        print(f"[Eval {eval_id}] Running with_skill...")
        with_dir = str(eval_dir / "with_skill" / "outputs")
        with_timing = run_single_eval(
            prompt, with_dir, use_skill=True,
            skill_path=str(skill_dir), model=args.model
        )
        (eval_dir / "with_skill" / "timing.json").write_text(json.dumps(with_timing, indent=2))
        status = "✅" if "error" not in with_timing else "❌"
        print(f"  {status} with_skill ({with_timing['duration_seconds']}s)")

        # Run without_skill (baseline)
        if not args.skip_baseline:
            print(f"[Eval {eval_id}] Running without_skill...")
            without_dir = str(eval_dir / "without_skill" / "outputs")
            without_timing = run_single_eval(
                prompt, without_dir, use_skill=False, model=args.model
            )
            (eval_dir / "without_skill" / "timing.json").write_text(json.dumps(without_timing, indent=2))
            status = "✅" if "error" not in without_timing else "❌"
            print(f"  {status} without_skill ({without_timing['duration_seconds']}s)")

    print(f"\nDone. Results in: {workspace}")
    print(f"To view: python -m eval-viewer.generate_review {workspace}")


if __name__ == "__main__":
    main()
