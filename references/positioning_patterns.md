# Article Positioning Patterns

Every angle proposed in Phase 1 is tagged with one of five **positionings**. Each has different default parameters AND a different writing shape. This file documents the shape.

Skill loads this file when Phase 1 selects a positioning. Phase 3 (drafting) uses the matching pattern as a structural skeleton.

---

## 思辨文 (Thesis piece)

**When to use**: one strong central judgment, expository argument that builds to a reframe.

**Default params**: 1500-2500 words, 2-3 blocks.

**Structural shape**:

```
① Opening hook — specific scene or surprising data
   (absolutely not a textbook-style abstract intro)
       ↓
② Reframe the problem — "most people think X, but I think Y"
       ↓
③ Evidence / mechanism — why Y holds
   (1-2 real examples, ideally from content_sources)
       ↓
④ Counter-voice acknowledged — address the strongest objection
       ↓
⑤ Conclusion that lingers — NOT a summary
   (a new question, a provocation, a callback to the opening)
```

**Writing重心**:
- Central judgment stated bluntly, defendable, possibly wrong — **take a position**
- The "reframe" in ② is the single most important move
- Avoid stacking multiple judgments; one sharp one > three fuzzy ones

**Common failure mode**: ending with "so let's all keep this in mind..." (hollow takeaway). Replace with callback or challenge.

---

## 攻略 (How-to guide)

**When to use**: step-by-step method, multi-layer teaching, reader should be able to execute after reading.

**Default params**: 3000-4500 words, 4-5 blocks.

**Structural shape**:

```
① Relatable pain — describe the reader's specific frustration
   ("你写 prompt 时遇到过这种情况吗...")
       ↓
② Framework overview — the layers or steps at a glance (pyramid block here)
       ↓
③ Each layer/step — dedicated section per layer:
    - Explanation
    - Concrete example (ideally from content_sources)
    - One actionable move the reader can try today
    - Optional: failure mode / learning curve honest note
       ↓
④ Integration — how the layers/steps fit together
   (another block — often flowchart or comparison)
       ↓
⑤ Takeaway checklist — explicit list of actions to carry home
   (not a "remember to X"-style summary, a literal checklist)
       ↓
⑥ Honest caveat — "this will feel clunky for the first week"
```

**Writing重心**:
- **Every section ends with an actionable step**. If a section only teaches concept without "do this today", the section is not攻略-grade yet.
- **Acknowledge learning curve**. Don't only paint successes ("用这个方法你也能...!"). Include "一开始会很笨拙" or "前三次尝试可能都不好用".
- **Humility scaffolding**. Open with "我也不确定对你有没有用" / "这是我个人的" — lowers the reader's defense and avoids the "我来教你"posture.
- **Recap arc**. Final section rehashes all action points and why they hang together.

**Common failure mode**: reads like a technical manual. Fix: thread personal story through the explanatory sections.

---

## 随笔 (Personal essay)

**When to use**: narrative forward, emotion forward, a personal take on a moment or theme.

**Default params**: 800-1500 words, 0-1 blocks.

**Structural shape**:

```
① Specific moment — a scene with texture
   (a concrete hour, a specific conversation, a detail that anchors the mood)
       ↓
② The thing that struck you — what made this moment matter
       ↓
③ A wider reflection — personal-to-cultural move
   (NOT "this made me realize that humans generally..."; more
    "I keep thinking about this because...")
       ↓
④ Return to the specific — end back near where you started,
   but with the view slightly shifted
```

**Writing重心**:
- **First-person is the structural backbone**. "我" appears constantly. The "I" is the camera.
- **No hidden argumentative structure**. If a随笔 tries to sneak in a "three-part argument" shape, it stops being a random.
- **Emotional arc over logical arc**. The reader should feel the mood shift, not follow a proof.
- **Minimal blocks**. A pyramid or flowchart in a随笔 breaks the voice. Use at most one, and only when a true structural element is embedded (e.g., "these three memories" → maybe a light comparison block).

**Common failure mode**: ending with a philosophical summary ("这让我想到人生的..."). Instead, end on a specific image or question.

---

## 评论 (Commentary / hot take)

**When to use**: fast response to an event, news, product launch, or viral phenomenon. Sharpness matters more than comprehensiveness.

**Default params**: 800-1500 words, 1-2 blocks.

**Structural shape**:

```
① Event — briefly say what happened
   (assume reader knows basics; don't re-explain news at length)
       ↓
② First-take reaction — your immediate gut response
   ("我看到的时候第一反应是...")
       ↓
③ Deeper analysis — the non-obvious layer you see
       ↓
④ Sharp judgment — take a side, state it
       ↓
⑤ Short kicker — a sentence that could be screenshotted
```

**Writing重心**:
- **Speed and sharpness**. A hedged评论 is worse than no评论.
- **Your take should contradict or complicate the mainstream narrative** — else why bother?
- **Avoid hedging phrases**: "从某种意义上说", "也许", "某种程度上". State the thing.
- **Screenshot-friendly close**. The last 1-2 sentences should be standalone quotable.

**Common failure mode**: neutral reporter tone ("各方观点如下"). Commentary is not journalism. Be biased, admit it.

---

## 翻译 (Translation with interpretation)

**When to use**: translating a foreign article with light annotation; not bare-bones translation, but translation-plus.

**Default params**: match source length, no blocks by default (add only if the source structure calls for it).

**Structural shape**:

```
① Short translator's note — why this article, why translating it now
       ↓
② Translated content — faithful to source meaning, fluent in Chinese
   (interspersed with):
       ↓
③ Cultural / context notes — where terms or references need unpacking for the Chinese reader
   (use [译注] markers or footnotes, not inline rewrites)
       ↓
④ Brief afterword — your take on what stood out, or where the original piece is wrong/dated
```

**Writing重心**:
- **Faithful to intent, not to syntax**. A clunky literal translation fails the source.
- **Mark cultural/language context explicitly** — don't silently localize references (e.g., don't translate "Thanksgiving" as "春节").
- **Add value beyond translation**. Pure translation is a pass-through; skilled translation adds the translator's judgment about why and what matters.
- **Don't hide behind the author**. Use the afterword to state your own position, even when it critiques the original.

**Common failure mode**: sentence-by-sentence literal translation that reads as machine-translated. Re-draft sentence rhythm in Chinese natively.

---

## Positioning mismatch mid-flight

If the user chose one positioning but the material demands another, **flag it and renegotiate**. Example:

> "You picked 思辨文 but the content you're giving me is all step-by-step instructions. That's more like a 攻略. Switching up would change the word count target (1500-2500 → 3000-4500) and block plan (2-3 → 4-5 blocks). OK to switch?"

This is a **Hard Block** in Auto Plan Mode — do not silently produce the wrong shape.

---

## Relationship to Khazix's five 原型

The five khazix 原型 (调查实验 / 产品体验 / 现象解读 / 工具分享 / 方法论分享) are **subcategories within 攻略 and 思辨文**, not separate positionings. They matter when the user is specifically writing in the khazix style; for other users, the 5 positionings above are enough.

Mapping:

| Khazix 原型 | Maps to |
|---|---|
| 调查实验型 | 攻略 + personal journey narrative |
| 产品体验型 | 评论 + personal journey narrative |
| 现象解读型 | 思辨文 |
| 工具分享型 | 攻略 with personal hook |
| 方法论分享型 | 攻略 |
