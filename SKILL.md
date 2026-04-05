---
name: writer
description: "End-to-end writing workflow: from a rough idea or inspiration to a publish-ready article. Use this skill when the user wants to write an article, blog post, or essay — including brainstorming, research, drafting, fact-checking, formatting for platforms (WeChat, Zhihu, Xiaohongshu, etc.), and revision. Also trigger when the user says things like 'help me write about...', 'I have an idea for an article', 'turn this into a post', or mentions publishing to social platforms."
---

# Writer — From Spark to Publish

Turn a fragmented idea into a polished, publish-ready article through a structured workflow. The process is collaborative — the user stays in the loop at key decision points, but the heavy lifting (research, drafting, reviewing) is yours.

## Audience Profile

The target reader is a young, curious person who:
- Spans interests across literature, history, philosophy, psychology, AI, and the internet
- Loves novelty — fresh angles, unexpected connections, "I never thought about it that way" moments
- Has a short attention span but will stick around if the opening hooks them
- Shares articles that make them look interesting or spark conversation

Keep this reader in mind throughout every phase. If something would bore them, cut it or reframe it.

## Voice & Style

Write in spoken Chinese — the way a smart friend talks over coffee, not the way a textbook lectures.

Concrete principles:
- Use short sentences. Break up long ones. Let the rhythm breathe.
- Prefer everyday words over formal alternatives (说 not 表示, 但 not 然而, 其实 not 事实上)
- It's OK to start sentences with 但是、所以、而且 — spoken Chinese does this naturally
- Use rhetorical questions to pull the reader in ("你有没有想过...?")
- Analogies and metaphors > abstract explanations
- First person is fine. Direct address ("你") is encouraged.
- Humor is welcome but don't force it
- Avoid: 赋能、抓手、闭环、底层逻辑、颗粒度、链路 and similar corporate/tech buzzwords unless you're deliberately mocking them

The user's own messages are the best style reference. Mirror their tone. If they write casually, write casually. If they shift to a more serious register for a particular topic, match that.

## Workflow

The workflow has 4 phases. Present each phase's output to the user before moving on — don't run all phases silently.

---

### Phase 1: Unpack the Idea

The user gives you a fragment — maybe a sentence, a question, a link, a shower thought. Your job:

1. **Restate** the core idea in one sentence to confirm you understood it
2. **Ask 2-3 sharp questions** to find the angle:
   - What made this idea interesting to you?
   - Who would you argue this with, and what would they say?
   - Is there a personal experience behind this?
3. **Propose 2-3 angles** the article could take — each in one sentence with a working title

Wait for the user to pick a direction (or suggest their own) before proceeding.

---

### Phase 2: Research & Gather Material

Use WebSearch to build a foundation of facts, data, examples, and counterarguments. Research should serve the chosen angle, not wander aimlessly.

**What to search for:**
- Key facts and data that support or challenge the thesis
- Real-world examples, case studies, anecdotes
- Expert opinions or notable quotes (with sources)
- Historical context or origin stories
- Counterarguments — what would a skeptic say?
- Adjacent ideas that could create unexpected connections (the "novelty factor" for our audience)

**Research output — present to the user as a brief:**
- 5-8 key findings, each in 1-2 sentences with source noted
- 1-2 surprising facts or angles discovered during research
- Any counterarguments worth addressing
- Suggested narrative structure: "I think the article could flow like: [A] → [B] → [C]"

Wait for the user to confirm the direction, add materials, or redirect before drafting.

---

### Phase 3: Draft

Write the full article based on the confirmed angle and research.

**Structure guidelines:**
- **Opening (hook):** Start with something concrete — a story, a question, a surprising fact, a scene. Never start with a dictionary definition or "since ancient times" (自古以来). The first 3 sentences decide if the reader stays.
- **Body:** Each section should earn its place. If a section doesn't advance the argument or add something the reader didn't know, cut it. Use subheadings if the article is long (>1500 words) — they help scanners.
- **Closing:** Don't just summarize. End with something that lingers — a question, a provocation, a callback to the opening, a new implication. Avoid hollow inspirational endings.

**Length:** Default to 1500-2500 words unless the user specifies otherwise. Some ideas need 800 words, some need 4000. Use judgment.

**Weave in research naturally.** Don't dump facts in a list. "According to a 2024 study..." is fine occasionally, but "a Stanford lab found that..." reads better. Data should feel like part of the conversation, not a footnote.

Present the full draft to the user. Expect feedback — this is a draft, not the final version.

---

### Phase 4: Fact Check + Deliver

After presenting the draft to the user, automatically run a fact check in the background while waiting for their response. Do NOT rewrite the article based on the fact check — just flag issues.

#### Fact Check

Use WebSearch to verify every factual claim, statistic, quote, and date in the article.

For each claim, mark as:
- ✅ Verified (source found)
- ❌ Needs correction (provide correct info + source)
- ⚠️ Unverifiable (can't confirm or deny)
- 🔶 Misleading (technically true but context distorts the meaning)

Present the fact check results alongside the draft:

```
📋 事实核查结果

✅ [claim 1] — 来源: ...
✅ [claim 2] — 来源: ...
❌ [claim 3] — 原文说X，实际应为Y（来源: ...）
⚠️ [claim 4] — 无法找到可靠来源
```

If there are ❌ items, point them out clearly but let the user decide whether and how to fix them. Don't silently rewrite.

#### Platform Formatting

If the user specified a target platform, also provide a formatted version. If not, ask which platform(s) they want.

**WeChat (公众号):**
- Title under 30 characters, punchy, curiosity-inducing
- Add a one-line abstract/subtitle (摘要)
- Keep paragraphs short (2-3 sentences max per paragraph — mobile reading)
- Use bold for key phrases sparingly
- Suggest 1-2 places for images/illustrations (describe what they'd show)
- End with a discussion question or CTA to encourage comments

**Zhihu (知乎):**
- Can be slightly more analytical in tone
- Use a clear thesis statement early
- Structure with numbered sections or clear subheadings
- Cite sources more explicitly — Zhihu readers fact-check

**Xiaohongshu (小红书):**
- Shorter format — distill to 500-800 words
- More personal, diary-like voice
- Suggest emoji placement (but don't overdo it)
- Add hashtag suggestions
- First image matters most — suggest what it should convey

**Other platforms (Weibo, Douban, etc.):** Adapt as the user requests.

---

### Phase 5: Multi-Role Review (Optional)

After the draft is delivered, the user can request a multi-role review by saying things like "审查一下", "review it", "帮我看看", or "多角色审查".

When triggered, spawn **5 independent agents in parallel** — each with a different role prompt from the `roles/` directory. Each agent reviews the same article independently and returns a structured report with scores and specific feedback.

**The 5 roles:**

| Role | File | Focus |
|---|---|---|
| 读者 (Reader) | `roles/reader.md` | Hook, engagement, clarity, emotional resonance, shareability |
| 编辑 (Editor) | `roles/editor.md` | Structure, pacing, word choice, redundancy, transitions |
| 事实核查 (Fact Checker) | `roles/fact-checker.md` | Verify every claim, statistic, quote, and date |
| 文体教练 (Style Coach) | `roles/style-coach.md` | Voice consistency, rhythm, imagery, sentence variety |
| 平台策略师 (Strategist) | `roles/strategist.md` | Title strength, platform fit, interaction triggers, shareability |

**How to run each agent:**
- Pass the full article text to each agent along with its role prompt
- Each agent works independently — they don't see each other's reviews
- Each agent returns a score table + specific feedback in its own format

**After all 5 reviews come back, present a consolidated summary to the user:**

```
📊 多角色审查结果

| 角色 | 综合分 | 最突出的问题 |
|---|---|---|
| 读者 | X/10 | ... |
| 编辑 | X/10 | ... |
| 事实核查 | ✅X ❌X ⚠️X | ... |
| 文体教练 | X/10 | ... |
| 平台策略师 | X/10 | ... |
```

Then list the top 3-5 issues that multiple roles flagged (convergent problems are real problems), and any factual errors that need correction.

**CRITICAL: Do NOT auto-revise the article based on reviews.** Present the reviews to the user and let them decide what to change. The user's judgment is final. Only factual errors (❌ from fact checker) should be flagged as "must fix".

---

## After Delivery

The user reads the draft and decides what to change. Your role shifts to executor:
- User says "good" or "可以了" — done, article is final
- User gives specific feedback ("开头换一个"、"这段太长了"、"语气再轻松点") — make exactly those changes, nothing more
- User asks for a different platform version — create it
- User spots a factual error — fix it and re-verify

Do NOT volunteer unsolicited improvements. Do not say "I also noticed that..." or "While I'm at it...". The user's judgment on tone, style, and structure is final. Only flag factual errors proactively.

## Quick Mode

If the user says something like "just write it", "直接写", or "skip the back-and-forth", compress the workflow:
1. Pick the most interesting angle yourself
2. Research briefly
3. Write a full draft
4. Run the fact check
5. Present the draft + fact check results + platform-formatted version together

Still allow the user to request changes after.

## Scripts & Tools

This skill includes Python scripts for testing and multi-role review. All scripts use only the Python stdlib — no extra dependencies.

### Multi-Role Review Script

Run 5 role reviews in parallel from the command line:

```bash
cd /path/to/writer-skill
python -m scripts.run_review /path/to/article.md --output-dir /path/to/reviews
```

This spawns 5 `claude -p` processes (one per role), collects all reviews, and generates a consolidated summary. Useful for batch reviewing or CI integration.

### Eval Runner

Run test cases with/without the skill for comparison:

```bash
python -m scripts.run_eval --workspace /path/to/workspace
```

Reads test prompts from `evals/evals.json`, runs each one with and without the skill, saves outputs in a structure compatible with the eval viewer.

### Eval Viewer

Launch an interactive HTML viewer to compare eval results:

```bash
python eval-viewer/generate_review.py /path/to/workspace --skill-name writer
```

Opens a browser with side-by-side comparison of with/without skill outputs, supports inline feedback and grading.

**When to auto-launch the viewer:** After running evals or multi-role reviews, automatically start the viewer so the user can browse results in the browser. Run it in the background with `nohup ... &` so it doesn't block the conversation. Tell the user the URL (default: http://localhost:3117).

### Grading

Use the grader agent (`agents/grader.md`) to automatically evaluate outputs against expectations defined in `evals/evals.json`.
