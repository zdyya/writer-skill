---
name: writer
description: |
  End-to-end Chinese writing workflow: from a rough idea to a publish-ready article with embedded HTML infographics. Guides Claude through 6 phases (idea unpacking → research → drafting → fact-check → illustration → multi-role review) and supports an Auto Plan Mode for one-shot execution.

  Trigger when the user says any of: 写文章 / 写稿子 / 帮我写 / 续写 / 扩写 / 公众号文章 / 长文 / 出稿 / 按我的风格写 / 帮我整理成稿子 / help me write an article / turn this into a post. Also triggers when the user hands over raw material (PDF, brief, link, voice transcript, scattered notes) with intent like 帮我写一篇 / 整理成文章.

  Do NOT use for: short social posts (小红书/推特/朋友圈 under 500 words), pure title or slogan generation, code documentation, literal translation without interpretive writing.
---

# Writer — From Spark to Publish

Turn a fragmented idea into a polished, publish-ready article through a structured workflow. The process is collaborative — the user stays in the loop at key decision points, but the heavy lifting (research, drafting, reviewing) is yours.

## Core Values (Tiebreakers When Rules Conflict)

Technical rules will sometimes conflict with each other — e.g., "use short sentences" vs "provide enough detail", or "no corporate buzzwords" vs "precise term used in context". When that happens, fall back to these four principles in order:

1. **Writing should read like a thinking human, not a textbook.** Specific scenes > abstract arguments. A real踩坑 story > ten well-reasoned bullet points. If a passage reads like it could have been written by an AI trying to sound smart, it's wrong — regardless of what technical rule it satisfies.

2. **Judgment > hedging.** The article should take a position. Not "X 也有道理 Y 也有道理", but "我觉得是 X，因为..." Even when that judgment might be wrong, state it clearly. Readers can disagree; they cannot engage with mush.

3. **Honest > complete.** It's better to say "我也不完全确定，但..." than to pretend certainty. It's better to say "这部分我没亲历过" than to invent an example. Partial honesty beats polished fakeness.

4. **Specific > abstract.** At every level — example, metaphor, word choice — prefer the concrete. "昨晚我又看了 3 小时短视频" > "现代人的注意力危机". "划走预言家" > "专业的内容评估师".

These four are the **top-level arbiters**. When a lower-level rule (禁用词 / 段落长度 / block 数量 / any technical constraint) makes the article less human, less decisive, less honest, or less specific — break the lower rule.

## Language Convention

This skill mixes English and Chinese intentionally. To keep it coherent, follow this rule when reading or editing any file:

| Surface | Language | Why |
|---|---|---|
| **Instructions / rules / structure** (this `SKILL.md`, `references/*.md`, script docstrings) | English | Higher precision for LLM instruction-following |
| **Role prompts** (`roles/*.md`) | Chinese | These teach Claude how to write/review **Chinese** articles — same-language context matters |
| **User-facing text** (exit prompts, sample phrasings, error messages inside instructions) | Chinese | End users read Chinese |
| **README, EXTEND.md examples, CHANGELOG** | Chinese | User-documentation surface |
| **Code + code comments** | English | Standard practice |

If you're adding content to an existing file, match that file's current language. If you're creating a new file, apply the table above. Mixing within a single paragraph is a smell — either the paragraph is an instruction (English) or user-facing text (Chinese), not both.

## User Extensions (Read First, Every Session)

Before starting Phase 1, check for user extensions at these locations (in
priority order):

1. `<cwd>/.writer-skill/EXTEND.md` — project-level
2. `~/.writer-skill/EXTEND.md` — user-level

### Case 1: File exists

Read it in full and let its directives override the defaults below.
**Don't mention the file to the user** — silent read, then proceed.

### Case 2: Neither file exists (likely a new user)

Offer **once, and only once** at the start of Phase 1, before proposing
angles. Use language close to this (adapt tone to the user):

> 我看你是第一次用 writer skill。有三件事我可以帮你**临时**定制这次写作（都可选，不填完全 OK）：
>
> 1. **风格参考**：你有没有 1-3 篇自己写过、最能代表你声音的文章？给我路径，我写稿前会读一遍做声音锚定。
> 2. **禁用词**：有没有你特别讨厌、不想在文章里出现的词？（默认已禁「赋能/抓手/闭环/底层逻辑/颗粒度/链路」）
> 3. **偏好平台+字数**：默认是公众号 1500-2500 字，要改吗？
>
> 这些都**可选**。你说"跳过"或直接告诉我文章想法，我就按默认走。如果你填了，我可以顺便帮你存成 `.writer-skill/EXTEND.md`，下次自动用。

Rules for this offer:

- **Ask once per session.** If the user skips or gives answers, never ask again in this conversation.
- **Never block on it.** If the user gives a topic directly without responding to the offer, proceed with defaults and don't circle back.
- **Don't auto-save without consent.** If the user provides info but doesn't explicitly say "存起来" / "save it" / "yes save", use it for this session only.
- **Treat in-memory config the same as file config.** For the rest of this session, whatever the user provided = their EXTEND.md.

### What EXTEND.md (or in-memory equivalents) can override

| Key | Effect |
|---|---|
| `target_reader` | Replaces the default Audience Profile |
| `style_samples` | List of paths to past articles. **Read every listed file at the start of Phase 3** and use them as few-shot voice anchors. Match cadence, sentence length, paragraph rhythm. **Purely for style**, not content. |
| `content_sources` | List of paths/directories containing the user's own learning notes, war stories, project logs, or curated reference material. **Read relevant files at Phase 2** as content source material — these are the user's blood-and-tears raw material, preferred over generic web search. Each source can be tagged `type: learning_notes / war_stories / reference`. |
| `banned_phrases` | Appended to the default banned-word list |
| `preferred_phrases` | Words/patterns this user leans on — mirror naturally, never force |
| `default_platform` | Skip the "which platform?" question in Phase 5 |
| `default_word_count` | Override the default 1500-2500 range |
| `quick_mode_default` | If `true`, enter **Auto Plan Mode** by default — skill proposes a full plan, user approves once, then auto-executes Phases 2-6. See "Auto Plan Mode" section below. |
| `auto_render_wechat` | If `true`, run `python -m scripts.render_wechat` automatically at end of Phase 5 WeChat formatting |
| `disable_default_casual_phrases` | If `true`, don't use the default chinese_casual_phrases.md word pool. Only use `preferred_phrases` the user explicitly set. Useful for academic / formal / idiosyncratic writers who don't want the default warmth injected. |

**`style_samples` vs `content_sources` — know the difference**:

- `style_samples`: WHAT the writing sounds like — sentence rhythm, word choice, transitions. Used in Phase 3 drafting.
- `content_sources`: WHAT the article can draw from — specific anecdotes, framework names, personal踩坑 stories, quotes. Used in Phase 2 research and Phase 6 auditing.

A user can have either, both, or neither. Missing `content_sources` = research fully via WebSearch. Missing `style_samples` = write in default voice. Missing both = fully generic writing, which is fine for first-timers.

See [`references/EXTEND.md.template`](references/EXTEND.md.template) for the full schema, and [`.writer-skill/EXTEND.md.example`](.writer-skill/EXTEND.md.example) for a minimal starter template the user can copy and edit.

## Audience Profile

*Default — overridden by `target_reader` in EXTEND.md if specified.*

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
- Avoid: 赋能、抓手、闭环、底层逻辑、颗粒度、链路 and similar corporate/tech buzzwords unless you're deliberately mocking them *(EXTEND.md can append via `banned_phrases`)*

The user's own messages are the best style reference. Mirror their tone. If they write casually, write casually. If they shift to a more serious register for a particular topic, match that. **If EXTEND.md provides `style_samples`, those files are the second-best reference — read them before drafting Phase 3 and consciously match their cadence.**

**Default 活人感 phrase pool** (for users without `preferred_phrases` set): See [`references/chinese_casual_phrases.md`](references/chinese_casual_phrases.md) for a curated list of turn-of-phrase expressions (转场 / 判断 / 自嘲 / 情绪 / 拉近 categories) that bring warmth to Chinese prose without making it sound performatively casual. Sprinkle 5-10 per 2000-word article, not more. Users can opt out with `disable_default_casual_phrases: true` in EXTEND.md.

### Demo prompts / example snippets inside the article

Articles often include example prompts (e.g. "a good身份 prompt looks like...") or short quoted snippets meant as templates for readers. These sections have a **different evaluation standard** than the surrounding prose:

- ✅ **Judge by "can a reader copy this into their own system prompt and have it work?"** — not by "does this sound poetic?"
- ❌ **Do NOT add literary flourish** — no fake-precise numbers ("the last 5% of attention"), no metaphor chains ("keep the quietest corner of a noisy world for them"), no nested definitive-sounding clauses ("listen for the half they didn't say")
- ✅ **Concrete scene language beats abstract imagery**: "someone who can hear 'I'm fine' and recognize it means 'I'm not'" beats "someone who protects the last remnant of authenticity in a shouting world"
- ✅ **Keep demo prompts short, parseable, and structurally simple** — the goal is demonstration, not performance

Why this matters: a prose-writer Claude defaults to "make this beautiful" when shown any blank space. Demo prompts are the one place in an article where **beauty is actively counterproductive** — they need to read like they came from someone who's iterated on real prompts, not from a poet.

## What AI Can and Can't Do (Boundary)

This skill is a style and structure generator, not a replacement for the user's judgment or experience. Being explicit about the boundary prevents the skill from overstepping — especially in Auto Plan Mode where there's no human in the loop for long stretches.

### ✅ AI handles well (delegate freely)

| Capability | Examples |
|---|---|
| **Finding evidence and counter-evidence** | "The user wants to argue X — search history, academic literature, culture for things that support and things that challenge it." |
| **Finding metaphors and analogies** | "Explain concept Y — give 3 candidate analogies, user picks one." |
| **Expanding from a confirmed angle** | "User already decided structure is A→B→C, each section's key point is given. AI fills in supporting detail." |
| **Background knowledge on named concepts** | Gestalt theory, Jungian shadow, Carl Rogers' three conditions, LLM basics — AI can state these correctly. |
| **Structural suggestions** | "This section feels slow — can I move part of it earlier?" — AI can diagnose and propose reorganizations. |

### ❌ AI must NOT do (will expose as fake if attempted)

| Category | Why |
|---|---|
| **First-hand observation or lived experience** | "我亲自买了 9.9 的 DeepSeek" / "我凌晨 3 点还在改这篇稿子" — these cannot be fabricated. Any attempt reads as hollow. |
| **Core creative angles** | The reframing insight that makes an article original (e.g. "AI 的灵魂感 = 用户感知错觉 + 高质量 prompt 工程") — AI can offer candidates but the judgment "yes, this is the take" must be the user's. |
| **Real emotional reactions** | "我当时愣住了" / "我鼻子一酸" — these require an actual event. Manufactured emotion is the single strongest AI smell. |
| **Value judgments on sensitive topics** | Which product is better, which ideology is right, who deserves credit — AI should describe the tradeoffs, not make the final call. |
| **The user's specific踩坑 stories** | These come from `content_sources` (v1.2+) or the user's in-conversation input. If neither has it, DO NOT invent a "一次我用 X 遇到 Y" story. |

### What to do when AI is about to overstep (especially in Auto Plan Mode)

**During Phase 3 drafting**, when approaching a section that needs first-hand material:

1. Check `content_sources` first — is there a relevant真实案例?
2. If yes → use it, cite internally (so source-auditor can verify in Phase 6)
3. If no → **explicitly flag in the draft**: "[TODO: 这里需要你自己的真实经历 / 具体数字 / 亲历场景]"
4. **Do NOT fabricate**. Marking TODO is better than inventing a plausible-sounding fake

At the end of Phase 3, if there are TODOs, surface them as a **Hard Block** (per Auto Plan Mode rules) — the user must fill them in before proceeding.

The principle: **AI writes the skeleton and connective tissue; the user supplies the blood.**

## Workflow

The workflow has 6 phases. Each phase MUST show a progress indicator on entry and a transition prompt on exit. Never run phases silently — the user should always know where they are and what's coming next.

### Progress Indicator (REQUIRED at the start of every phase)

Display this progress bar at the START of every phase output:

```
---
📍 **Phase X/6: [中文阶段名]** | ① 解题 → ② 调研 → ③ 初稿 → ④ 核查 → ⑤ 配图 → ⑥ 审查
---
```

Rules:
- Use ✅ to mark completed phases, **bold** for the current phase, plain text for upcoming phases
- Example for Phase 3: `✅① 解题 → ✅② 调研 → **③ 初稿** → ④ 核查 → ⑤ 配图 → ⑥ 审查`
- In Auto Plan Mode, still show progress — just advance without user confirmation between phases

### Transition Prompt (REQUIRED at the end of every phase)

After presenting each phase's output, ALWAYS end with a boxed transition prompt:

```
> **下一步 → Phase X: [名称]**：[一句话说明下一步做什么]
> [需要用户做什么：选择方向 / 确认素材 / 说"继续"/ etc.]
```

This prevents the user from ever wondering "is it done?" or "what do I do now?"

---

### Phase 1: 解题（Unpack the Idea）

The user's input can range from a single fragment ("独处") to a fully-spec'd brief ("结合 X 课程写一篇关于 Y 的公众号文章"). Your job is to produce 2-3 candidate angles and let the user pick one. **The amount of upfront clarification should match how complete the input is** — don't over-interrogate a user who already told you exactly what they want.

#### Silently classify the input

Count how many of these three signals the user's message contains:
- **Topic**: what the article is about
- **Source**: what material grounds it (book, course, notes, personal experience, link)
- **Type**: what kind of output (article / post / essay / short piece)

Also factor in what's already set by EXTEND.md (platform, word count, target reader) — these don't need to be asked again.

#### Article positioning (applied to every candidate angle)

Every angle you propose should be implicitly tagged with an **article positioning**. Different positions have different default parameters:

| Positioning | 中文 | Default words | Density | Config blocks | When to use |
|---|---|---|---|---|---|
| `思辨文` | Thesis piece | 1500-2500 | 2-3 blocks | Comparison + key data viz | Central argument, one strong judgment |
| `攻略` | How-to guide | 3000-4500 | 4-5 blocks | Multiple frameworks, each a block | Step-by-step methods, multi-layer teach |
| `随笔` | Essay / personal | 800-1500 | 0-1 blocks | Usually no blocks | Narrative, emotion-forward, personal |
| `评论` | Commentary | 800-1500 | 1-2 blocks | One sharp take block | Hot takes on events/news/products |
| `翻译` | Translation | — (match source) | Match source | — | Translating + lightly annotating a foreign article |

**How to apply positioning**:
- Default: `思辨文` (unless EXTEND.md or user input suggests otherwise)
- Mention the positioning next to each candidate angle, e.g. "Angle A 适合写成 **思辨文**（约 1800 字，2 张 block）"
- If the user's input is clearly a how-to ("帮我写一个 X 的攻略"), auto-switch to `攻略` positioning and mention it
- User can override by saying "写成攻略" or "写短一点的随笔"
- **Mid-flight positioning change**: if the user mid-draft says "我要攻略不是思辨文", re-negotiate字数 and 配图密度 before continuing — don't just add more words

Positioning is not a question to ask the user — it's a **default you propose** with each angle, and the user can accept or override.

**Each positioning has a specific writing shape**. See [`references/positioning_patterns.md`](references/positioning_patterns.md) for the full structural pattern per positioning — Phase 3 drafting should follow the matching pattern (opening type, section flow, ending style, common failure modes).

#### Three paths based on signal count

**HOT (3/3 signals present)** — skip restatement and sharp questions. Go straight to:

1. **2-3 candidate angles**, each with a working title + one-sentence hook
2. **Your recommendation** (one-line reason for the pick)
3. **Ask the user to pick** one (or propose their own)

Optionally add ONE soft sidebar line AFTER the angles, not as a blocking question:
> "顺便：如果你有踩过的具体坑或真实经历，告诉我会让初稿更具体（不说也可以）。"

This sidebar is for users who want to add texture, not a mandatory question.

**WARM (2/3 signals)** — minimal clarification, then angles:

1. **One-sentence restatement** of what you understood (in case you got a detail wrong)
2. **One targeted question** about the missing signal (e.g., "你想写长文章还是短评?")
3. **2-3 candidate angles**
4. Ask user to pick

**COLD (1/3 signals or pure fragment)** — full classic flow:

1. **Restate** the core idea in one sentence
2. **Ask 2-3 sharp questions**:
   - 什么让这个想法打动你？
   - 你会跟谁争论这个观点，对方会怎么说？
   - 背后有具体经历吗？
3. **2-3 candidate angles**
4. Ask user to pick

**Exit prompt (all paths):** User must pick an angle (A/B/C or their own proposal). Do NOT proceed to Phase 2 until they respond.

---

### Phase 2: 调研（Research & Gather Material）

Build a foundation of facts, data, examples, and counterarguments. Research should serve the chosen angle, not wander aimlessly.

#### Source priority (CRITICAL)

Pull material in this order — earlier sources preferred over later ones:

1. **User's `content_sources`** (if EXTEND.md specifies): Read relevant files in full. These are the user's own war stories, learning notes, curated references — highest authority and most distinctive material
2. **WebSearch**: For facts, data, expert quotes, counterarguments not covered in content_sources
3. **General knowledge**: Last resort, and always flag as `[inferred]`

If a user has `content_sources` but you skip straight to WebSearch, the resulting article will be **structurally shallow** — it will miss the user's unique angle. This is the most common cause of "the draft feels generic."

#### What to search/gather

- Key facts and data that support or challenge the thesis
- Real-world examples, case studies, anecdotes
- Expert opinions or notable quotes (with sources)
- Historical context or origin stories
- Counterarguments — what would a skeptic say?
- Adjacent ideas that could create unexpected connections (the "novelty factor" for our audience)

#### Source reliability tagging (required in the brief)

When presenting findings, **tag each one** with its reliability tier:

| Tag | Meaning | Example |
|---|---|---|
| `[一手]` / `[primary]` | Direct source verified — original paper, official statement, user's own material | JAMA 2023 paper, Rogers 1957 publication, user's own blog post |
| `[二手]` / `[secondary]` | Reputable translation or coverage of a primary source | Tech media's report on a study, Wikipedia article |
| `[转述]` / `[paraphrased]` | Second-hand paraphrase — likely accurate but not verbatim | "Someone said the founder of X company once said..." |
| `[推断]` / `[inferred]` | Your own inference from the pattern, not directly sourced | "Based on industry trends, it seems likely that..." |

**Tags are mandatory.** If you can't categorize a finding, search again until you can. Phase 4 fact-check will prioritize verifying `[转述]` and `[推断]` findings — those are where hallucinations hide.

#### Research output — present to the user as a brief

- **5-8 key findings**, each 1-2 sentences with source noted AND tag `[一手]/[二手]/[转述]/[推断]`
- **1-2 surprising facts or angles** discovered during research
- **Counterarguments worth addressing**
- **Suggested narrative structure**: "I think the article could flow like: [A] → [B] → [C]"

**Exit prompt:** Ask the user to confirm the direction, add materials, or redirect. Do NOT start drafting until they respond.

---

### Phase 3: 初稿（Draft）

Write the full article based on the confirmed angle and research.

**Structure guidelines:**
- **Opening (hook):** Start with something concrete — a story, a question, a surprising fact, a scene. Never start with a dictionary definition or "since ancient times" (自古以来). The first 3 sentences decide if the reader stays.
- **Body:** Each section should earn its place. If a section doesn't advance the argument or add something the reader didn't know, cut it. Use subheadings if the article is long (>1500 words) — they help scanners.
- **Closing:** Don't just summarize. End with something that lingers — a question, a provocation, a callback to the opening, a new implication. Avoid hollow inspirational endings.

**Length:** Default to 1500-2500 words unless the user specifies otherwise. Some ideas need 800 words, some need 4000. Use judgment.

**Weave in research naturally.** Don't dump facts in a list. "According to a 2024 study..." is fine occasionally, but "a Stanford lab found that..." reads better. Data should feel like part of the conversation, not a footnote.

**Exit prompt:** Present the draft, then tell the user: "接下来我会做事实核查。你可以先看稿子，有修改意见随时说。说'继续'我开始核查。"

---

### Phase 4: 核查（Fact Check）

Run the fact check immediately after the user confirms (or alongside the draft presentation if user said "继续"). Do NOT rewrite the article based on the fact check — just flag issues.

Use WebSearch to verify every factual claim, statistic, quote, and date in the article.

For each claim, mark as:
- ✅ Verified (source found)
- ❌ Needs correction (provide correct info + source)
- ⚠️ Unverifiable (can't confirm or deny)
- 🔶 Misleading (technically true but context distorts the meaning)

Present the fact check results:

```
📋 事实核查结果

✅ [claim 1] — 来源: ...
✅ [claim 2] — 来源: ...
❌ [claim 3] — 原文说X，实际应为Y（来源: ...）
⚠️ [claim 4] — 无法找到可靠来源
```

If there are ❌ items, point them out clearly but let the user decide whether and how to fix them. Don't silently rewrite.

**Exit prompt (MANDATORY):** After presenting the fact check, you MUST proactively prompt for Phase 5:

> **下一步 → Phase 5: 配图**：识别文章里的结构段（对比 / 层级 / 流程 / 嵌套），用 HTML 信息图替代散文表达，然后渲染成微信公众号兼容的 HTML。
> 说"继续"开始，或者说"跳过配图"直接做平台排版，或者"跳过"直接进审查。

---

### Phase 5: 配图（Illustration）

This is where the article becomes visually publishable. Two sub-steps:
(1) generate infographics for structural paragraphs, (2) produce the
platform-ready output (HTML for WeChat, markdown for others).

**CRITICAL PRODUCT POSITIONING**: 配图 is the defining feature of this
Skill over a pure-text writer. Treat it as a first-class creative step,
not a formatting afterthought. Give it its own airtime in the output.

#### 5a. Infographics (信息架构师)

Run the **info-architect** role from `roles/info-architect.md`. It scans
the article for paragraphs with "invisible structure" — language signals
like "two kinds", "three layers", "four steps", nested logic — and
replaces them with one of four HTML infographic block types:

| Block | Use for |
|---|---|
| `:::comparison` | 2–3 side-by-side cards (对比) |
| `:::pyramid` | Multi-tier hierarchy (层级) |
| `:::flowchart` | N-node horizontal flow (流程) |
| `:::nested` | Concentric nested boxes (嵌套) |

The info-architect role is a **BUILDER**, not a reviewer — it modifies the
article rather than commenting on it. Run it standalone (not as part of
the Phase 6 parallel review).

Workflow:
1. Info-architect reads the article, proposes candidate blocks
   (position + type + rationale) without writing JSON yet
2. **Present the candidate list to the user** and wait for confirmation on
   which to keep. Default cap: **3-4 blocks per 2000-word article** —
   over-visualization breaks reading rhythm
3. For confirmed candidates, write the JSON block bodies using the
   article's exact wording (no paraphrasing, no invented data)
4. Insert blocks AFTER the corresponding paragraph (they supplement, not
   replace)
5. Save the illustrated version as `<slug>-wechat.md`

**Why HTML/CSS instead of image-model-generated images**: image models
can't spell, can't align pixels, can't keep style consistent across
images, and cost money per regeneration. HTML blocks deliver 100% text
accuracy, zero cost, and let you edit a number by editing JSON. Only use
actual images for cover art, photography, or atmosphere — never for
structured information.

#### 5b. Platform Formatting

If the user specified a target platform, produce the formatted version(s).
If not, ask which platform(s) they want. Default to WeChat if
`default_platform` is set in EXTEND.md.

**WeChat (公众号):**
- Title under 30 characters, punchy, curiosity-inducing
- Add a one-line abstract/subtitle (摘要)
- Keep paragraphs short (2-3 sentences max — mobile reading)
- Use bold for key phrases sparingly
- End with a discussion question or CTA to encourage comments
- **Render to HTML**: run `python -m scripts.render_wechat <slug>-wechat.md --open`
  which produces a single self-contained HTML file with inline-style-only
  elements (table layout, no flex/grid), plus a one-click copy button in
  the browser preview. Paste into the WeChat editor — formatting survives.
  This is the default for WeChat; do not fall back to pure markdown.

**Zhihu (知乎):**
- Can be slightly more analytical in tone
- Use a clear thesis statement early
- Structure with numbered sections or clear subheadings
- Cite sources more explicitly — Zhihu readers fact-check
- Markdown output is fine (no HTML renderer needed yet)

**Xiaohongshu (小红书):**
- Shorter format — distill to 500-800 words
- More personal, diary-like voice
- Suggest emoji placement (but don't overdo it)
- Add hashtag suggestions
- First image matters most — suggest what it should convey

**Other platforms (Weibo, Douban, etc.):** Adapt as the user requests.

**Exit prompt (MANDATORY):** After presenting the illustrated article +
platform output, you MUST proactively prompt for Phase 6:

> **下一步 → Phase 6: 多角色审查**：5 个独立视角（读者、编辑、事实核查、文体教练、平台策略师）同时审稿（已带图、已排版），帮你找出可能忽略的问题。
> 说"审查一下"开始，或者说"跳过"直接定稿。

Do NOT skip this prompt. Do NOT end the conversation here. Always guide the user to the final phase.

---

### Phase 6: 审查（Multi-Role Review）

When the user confirms (says "审查一下", "review", "帮我看看", "继续", etc.), spawn **all reviewer agents in parallel** — each with a different role prompt auto-discovered from the `roles/` directory (excluding builder roles like `info-architect`). Each agent reviews the same article independently and returns a structured report with scores and specific feedback.

If the user says "跳过" or "不用了", skip this phase and confirm the article is final.

**The reviewer roles (auto-discovered from `roles/*.md`, excluding builders):**

| Role | File | Focus | Runs when |
|---|---|---|---|
| 读者 (Reader) | `roles/reader.md` | Hook, engagement, clarity, emotional resonance, shareability | Always |
| 编辑 (Editor) | `roles/editor.md` | Structure, pacing, word choice, redundancy, transitions | Always |
| 事实核查 (Fact Checker) | `roles/fact-checker.md` | Verify every claim, statistic, quote, and date | Always |
| 文体教练 (Style Coach) | `roles/style-coach.md` | Voice consistency, rhythm, imagery, sentence variety | Always |
| 平台策略师 (Strategist) | `roles/strategist.md` | Title strength, platform fit, interaction triggers, shareability | Always |
| 素材审计师 (Source Auditor) | `roles/source-auditor.md` | How well does the draft use the user's own `content_sources` — catches "article is shallow because author's own material wasn't used" | Only if `content_sources` exists in EXTEND.md |

The `run_review.py` script auto-discovers these via `roles/*.md`, so adding new reviewer roles = drop a `.md` file in `roles/`. No code changes needed. Builder roles (like `info-architect`) are excluded via the `BUILDER_ROLES` constant in that script.

**How to run each agent:**
- Pass the full article text to each agent along with its role prompt
- Each agent works independently — they don't see each other's reviews
- Each agent returns a score table + specific feedback in its own format

**⚠️ Simulation vs real parallel run:**

There are two ways this phase can execute:

1. **Real parallel** (preferred): Use `scripts/run_review.py` which spawns one `claude -p` subprocess per role. Each agent starts with a blank context and is genuinely independent.
2. **In-conversation simulation**: A single Claude instance plays all 5 roles sequentially. This happens when the user is running the skill inside a single chat without scripts.

**Simulation mode has known biases**:
- Scores tend to be **systematically higher** than real parallel runs (average 7-9 range instead of 5-9) because one model playing all roles subconsciously avoids contradicting itself
- "Independent" is not truly independent — earlier role outputs contaminate later ones
- The fact-checker role is especially unreliable in simulation (may repeat Phase 4 findings without re-verifying)

If you are in simulation mode, **explicitly disclose this to the user before presenting the review**. Suggested phrasing: "再次声明：一人扮 5 角的模拟版，分数可能有自我鼓励偏差，但独立视角尽量做到了。"

For high-stakes articles, recommend the user run the real parallel version via `python -m scripts.run_review <article>.md` after the conversation.

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

**Exit prompt:** "审查完成。以上是5位审稿人的反馈。你可以告诉我要改哪些，或者说'定稿'完成。"

---

## After Delivery

The user reads the output and decides what to change. Your role shifts to executor:
- User says "good", "可以了", or "定稿" — done, article is final
- User gives specific feedback ("开头换一个"、"这段太长了"、"语气再轻松点") — make exactly those changes, nothing more
- User asks for a different platform version — create it
- User spots a factual error — fix it and re-verify

Do NOT volunteer unsolicited improvements. Do not say "I also noticed that..." or "While I'm at it...". The user's judgment on tone, style, and structure is final. Only flag factual errors proactively.

## Four-Layer Self-Audit Protocol

An alternative to Phase 6 multi-role review. Phase 6 is broader and more subjective; this protocol is **narrower, more mechanical, more reliable**. Use it when:

- **Auto Plan Mode** is running (default self-audit in automatic execution)
- The user requests a **quick check** instead of full multi-role review ("帮我快速自审一下")
- You want to **pre-check a draft before Phase 6** to catch obvious issues first

### Layer structure

Four layers, run in order. Each has a clear pass/fail standard. A draft passes only when all four pass.

#### L1 — Hard Rules Scan (automated)

Purely mechanical scans. Any hit must be fixed before proceeding. No judgment calls.

**L1-1 Banned phrase scan** (against default banned list + user's `banned_phrases` from EXTEND.md):
- Default banned: 赋能、抓手、闭环、底层逻辑、颗粒度、链路、心智、打法、赛道、范式、底层能力、方法论
- Also flag: 说白了、意味着什么、这意味着、本质上、换句话说、不可否认、综上所述、值得注意的是、不难发现
- Fix: replace with preferred alternative or rephrase

**L1-2 Structural cliché scan**:
- "让我们来看看..." / "接下来让我们..."
- "在当今...的时代" / "随着...的发展"
- "首先...其次...最后" (unless genuinely enumerating 3 parallel items)
- Consecutive bullet points (>3) where prose would flow better

**L1-3 Vague tool names**:
- "AI 工具" / "某个模型" / "相关技术" — all must be replaced with specific product names (Claude, GPT-4, Stable Diffusion, etc.)

**L1-4 Style sample placeholders**:
- Any `[TODO]` / `[填入真实经历]` / `[example]` markers left over from drafting
- These are Hard Blocks — user must fill in before finalizing

**Pass**: zero hits across L1-1 to L1-4.

#### L2 — Style Consistency Check (pattern matching)

Compare the draft against the user's style anchor (`style_samples` if provided, or default chinese_casual_phrases).

**L2-1 Opening check**:
- ✅ Opens with specific scene/event/question/surprising fact
- ❌ Opens with "自古以来 / 在当今时代 / XX 是一个 Y" textbook patterns

**L2-2 Rhythm check**:
- ✅ Short-long sentence alternation (no ≥3 consecutive sentences of same length)
- ✅ At least 2-3 standalone one-sentence paragraphs (creates rhythm breaks)
- ✅ Questions used for pivoting ("为什么？" / "那怎么办？")

**L2-3 Colloquial ratio**:
- Uses ≥5 distinct phrases from user's `preferred_phrases` or `references/chinese_casual_phrases.md`
- No sentence reads like it was machine-translated from English

**L2-4 Paragraph length**:
- Mobile-reading friendly: paragraphs avg 2-4 sentences, max ~80 chars per paragraph
- Exception: code blocks and quoted material

**Pass**: L2-1 passes + at least 3/4 of L2-2/2-3/2-4 pass.

#### L3 — Content Depth Check (judgment-based)

**L3-1 Claim grounding**:
- Every major claim has at least one of: specific person, scene, number, citation. No floating claims.

**L3-2 Knowledge delivery style**:
- Facts and frameworks appear as "as it happens, this is..." rather than "let me now explain..."
- No textbook-style definition dumps

**L3-3 Content_sources utilization** (if `content_sources` is set):
- At least 40% of the user's blood-and-tears material is referenced
- Key 元洞察 from content_sources is lifted into the article (not merely mentioned)
- If < 40% utilized → flag as ⚠️ source-underused (not a Hard Block but visible in final report)

**L3-4 Counterargument handling**:
- The strongest objection to the article's thesis is addressed somewhere, not avoided
- Done in "I also thought X, but..." form rather than "some people say X, which is wrong"

**L3-5 Positioning-specific check** (per `references/positioning_patterns.md`):
- **攻略**: every section ends with an actionable step; learning curve and failure modes acknowledged
- **思辨文**: central judgment stated clearly; at least one reframing insight
- **随笔**: emotional arc present; no hidden argumentative structure pretending to be narrative
- **评论**: personal first-take at opening; deeper analysis in middle
- **翻译**: cultural/language notes where source context matters

**Pass**: L3-1 + L3-2 must pass. L3-3 to L3-5 pass when applicable (skip if not relevant to this piece).

#### L4 — Humanness Final Review (subjective, single judgment)

Read the whole article. Ask one question:

> **"Does this feel like a thoughtful person genuinely caring about something and explaining it to me, or like an AI producing output that looks like that?"**

Specific lenses:

**L4-1 Temperature**: Does the emotional language feel somatic ("我当时愣住了") or performed ("this is truly profound")?

**L4-2 Uniqueness**: Could 10 other AI writing skills have produced the same article? If yes, the specificity of viewpoint is missing.

**L4-3 Posture**: Does the writer sound like "a peer sharing what they figured out" or "a teacher instructing you" / "a brand doing marketing"?

**L4-4 Flow**: Reading end-to-end, any section where attention drops or the reader has to re-read to follow the logic? Those are rhythm breaks.

**Pass**: overall impression of "yes, this reads like a human thinking". If any single lens registers as AI-smelling, mark the specific paragraph and return to Phase 3 for revision.

### Output format

After completing L1-L4, output a compact audit report:

```
## 🔍 四层自检报告

**L1 硬性规则** ✅ / ❌
- 禁用词：X 处命中（已修复 / 待修复）
- 结构套话：X 处
- 空泛工具名：X 处
- [TODO] placeholders: X 处 ← Hard Block if > 0

**L2 风格一致性** ✅ / ❌
- 开头：✅
- 节奏：✅（N 处一句成段）
- 口语化：✅（使用 N 个偏好词）
- 段落长度：✅

**L3 内容深度** ✅ / ❌
- 观点支撑：✅
- 知识输出方式：✅
- content_sources 使用率：N%（⚠️ 低于 40%）
- 反方观点：✅
- 定位专项（攻略）：✅ 每节有行动点 / ❌ 第 X 节缺行动点

**L4 活人感** ✅ / ❌
- 温度：✅
- 独特性：✅
- 姿态：✅（同辈分享，不居高临下）
- 心流：✅ / ❌（第 X 段需要回读）

**总评**: 4 层全通过 / X 层需返工
**Hard Block (if any)**: [TODO] 未填 / 事实错误 / L1 禁用词未替换
**优先修复**: [top 1-3 items]
```

### How it slots into the workflow

- **Auto Plan Mode**: after Phase 5 (render), run L1-L4 silently. Surface the report at the very end with the delivery artifacts. If L1 or L3 has Hard Blocks, pause Auto Plan and surface to user.
- **Interactive mode**: run L1-L4 before Phase 6 as a pre-check. Issues caught here save Phase 6 reviewers from flagging obvious fixable problems.
- **Quick audit standalone**: when user says "帮我快速自审一下" instead of full Phase 6, run just L1-L4.

## Auto Plan Mode (replaces old Quick Mode)

The default 6-phase flow has a user confirmation point after every phase — good for high-touch writing, but too many decisions for users who want a one-shot draft. **Auto Plan Mode** is the fix.

### When to enter Auto Plan Mode

Triggered by any of:

- User says `--auto` / "自动跑" / "一把梭" / "直接到底" / "全自动"
- User says something like "我就想要一篇文章，不想来回沟通"
- User explicitly asks for a draft without approvals
- **EXTEND.md has `quick_mode_default: true`** — enter Auto Plan Mode by default, unless the user explicitly says "一步一步来" or "我想全程参与" this session

### Core design: Plan first, one approval, then full ReAct

```
User input
  ↓
[Phase 1 ONLY: Auto Plan Mode Inception]
  Read EXTEND.md + content_sources index + user input
  Silently classify positioning + pick best angle + outline sources
  ↓
[Present Execution Plan] ⛔ one approval point
  ↓
User: "ok" / "改 [某项]"
  ↓
[ReAct mode: Phase 2 → 3 → 4 → 5 → 6] (no user confirmation)
  Skill acts as its own observer at each step
  Only surfaces to user on Hard Block
  ↓
[Final Delivery] all artifacts at once
```

### The Execution Plan (what gets approved once)

Present this in a single boxed block after input:

```markdown
📋 Execution Plan

Topic: <topic>
Positioning: <思辨文/攻略/随笔/评论/翻译>
Angle: <one-sentence selected angle + one-line why>
Target reader: <from EXTEND.md or default>

[Research]
- Sources: <WebSearch × N> + <content_sources 文件清单，如果有>
- Key questions to answer: <3-5 bullet points>

[Draft]
- Word count target: <from positioning table>
- Structure: ① hook → ② <arg 1> → ③ <arg 2> → ④ counter → ⑤ close

[Infographics]
- Plan: <N> blocks
- Types: <comparison × K, pyramid × K, ...>
- Anchor paragraphs: <brief list>

[Review]
- Run parallel reviewers: <list — include source-auditor iff content_sources exists>
- Mode: <real parallel via run_review.py | simulated in-conversation>

[Delivery]
- markdown: <path>
- HTML: <path>
- Review report: <path>

Estimated total runtime: <X minutes>

说 "ok" 开始自动执行。如需调整：告诉我改哪项（比如 "换角度 B" / "字数 3000" / "跳过审查"）。
```

### Hard Block conditions (when Skill MUST come back to user)

During automatic execution, skill self-monitors and breaks back to user ONLY when:

| Condition | Reason |
|---|---|
| **Phase 4: ❌ fact error found** | User must decide whether to fix or accept |
| **Phase 2: 关键素材完全缺失** (can't find evidence for a claim the angle depends on) | Angle may not be viable, user needs to redirect |
| **Phase 5: block JSON 构造失败 2 次以上** | Degrade gracefully to no-blocks mode, confirm with user |
| **Phase 6: source-auditor 标红 🚨** (< 40% material usage + content_sources has content) | Draft is shallow because material wasn't used, user should decide redraft |
| **Positioning mid-flight mismatch** (halfway through, realize 思辨文 should be 攻略 based on user's specs) | Word count / blocks plan needs renegotiation |

**Anything else** — missing data points, debatable word choice, minor structural questions — skill decides itself based on the plan and keeps going. The purpose of Auto Mode is to eliminate **all non-critical interruptions**.

### ReAct self-observation protocol

At each phase end in auto mode, skill silently runs a **self-audit checklist** (not shown to user unless it triggers a hard block):

| Phase | Self-audit question |
|---|---|
| Phase 2 | "Did I find `[一手]` evidence for each key claim in my angle?" → if no, search more before moving on |
| Phase 3 | "Does the draft match the plan's word count ±20% and section structure? Any `[TODO]` placeholders left?" → if TODOs exist → Hard Block; if word count off → revise |
| Phase 4 | "Any ❌ errors?" → if yes, hard block; otherwise proceed |
| Phase 5 | "Do rendered blocks read correctly? Any error cards?" → if yes, retry once then hard block |
| **Phase 6** | **Run Four-Layer Self-Audit Protocol (L1-L4) in place of multi-role review.** The four layers replace the 6-role simulation in Auto Plan Mode because they're more mechanical and don't suffer from the self-scoring bias of simulated multi-role. |

If the user wants real multi-role review instead, they should switch to interactive mode or run `python -m scripts.run_review` separately after Auto Plan completes.

This replaces user-as-observer with skill-as-observer. The flow becomes:
`Thought → Action → Self-Observation → (block? or next Thought)`

Which is proper ReAct.

### Final delivery format

After auto run completes, present everything at once:

```markdown
✅ Auto Plan 执行完成

📊 执行摘要
- Phase 2: <N> searches, <K> findings
- Phase 3: draft <word_count> words
- Phase 4: <N> ✅, <M> ⚠️, <L> ❌ (if any ❌, should have hard-blocked earlier)
- Phase 5: <N> blocks rendered, 0 errors
- Phase 6: avg score <X>/10

📄 Artifacts
- Markdown: <path>
- HTML: <path>
- Review report: <path>

🚨 要你看一眼的地方 (如果有)
- <hard block 条目 / Phase 6 低分项 / Phase 4 ⚠️ 转述类条目>

接下来: 说 "定稿" 结束流程，或说 "改 [某处]" 我继续迭代。
```

### Fallback

If user says "改" without specifying, exit Auto Mode and revert to the default 6-phase interactive flow for all subsequent changes. Auto Mode is a one-shot acceleration, not a permanent state.

## Claude Code Plan Mode compatibility

**Known limitation:** If the user invokes this skill while Claude Code is in Plan Mode (the built-in `/plan` feature that restricts file writes and shell execution), the skill cannot complete Phases 3-6 (which require writing markdown, running `render_wechat.py`, and optionally spawning `run_review.py` subprocesses).

Behavior in Claude Code Plan Mode:

- Phase 1 (解题): ✅ Full functionality
- Phase 2 (调研): ✅ WebSearch works, but can't save intermediate research to file
- Phase 3 (初稿): ⚠️ Can draft in conversation but not save to file
- Phase 4 (核查): ⚠️ WebSearch works, can't modify article
- Phase 5 (配图): ❌ Can't run `render_wechat.py`; block JSON can be shown inline
- Phase 6 (审查): ❌ `run_review.py` needs subprocess; only in-conversation simulation works

**Recommendation in Plan Mode**: tell the user "We're in Plan Mode. I can walk you through Phases 1-2 and sketch the structure, but to actually draft + render + review we need to exit plan mode. Want to continue in plan-only, or exit first?"

## Scripts & Tools

This skill includes Python scripts for testing and multi-role review. All scripts use only the Python stdlib — no extra dependencies.

### Multi-Role Review Script

Run all reviewer roles in parallel from the command line:

```bash
cd /path/to/writer-skill
python -m scripts.run_review /path/to/article.md --output-dir /path/to/reviews
```

This spawns one `claude -p` process per reviewer role (auto-discovered from
`roles/*.md`, excluding builder roles like `info-architect`), collects all
reviews, and generates a consolidated summary. Useful for batch reviewing
or CI integration.

### WeChat HTML Renderer

Convert a markdown article (optionally containing `:::type` infographic
blocks) into WeChat-editor-compatible HTML:

```bash
python -m scripts.render_wechat /path/to/article.md --open
```

Output is a single self-contained HTML file:
- Body uses inline styles + `<table>` layout only (the safe subset the
  WeChat editor preserves on paste)
- Preview page has a one-click copy button that selects only the article
  body (the toolbar/JS itself is stripped on copy)
- Infographic blocks (`:::comparison`, `:::pyramid`, `:::flowchart`,
  `:::nested`) are rendered as styled cards, not images

See `scripts/RENDER_WECHAT.md` for the block DSL reference and the LLM
prompt that drives auto-insertion of infographics during Phase 5.

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
