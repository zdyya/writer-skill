# WeChat-Compatible HTML Renderer

`render_wechat.py` converts a markdown article into a self-contained HTML file
that can be copy-pasted into the WeChat public-account editor without losing
formatting.

## Why

WeChat's editor strips `class` attributes and external CSS. It only preserves
inline styles on a narrow set of tags, and breaks on modern layout primitives
like `flex`/`grid` in some mobile clients. This script produces output that
sticks to the safe subset:

- Every element carries its full style as an `inline style` attribute
- Layout uses `<table>` + `border-spacing`, never `flex` or `grid`
- System font stack lets WeChat render with its own PingFang/YaHei
- No `class`, no external CSS, no `<link>` — all styles are self-contained

The output page wraps the article in a preview shell with a **one-click copy
button** that selects only the article body. The toolbar/JS itself is not
copied.

## Usage

```bash
# From the repo root
python -m scripts.render_wechat path/to/article.md

# Custom output path
python -m scripts.render_wechat path/to/article.md -o /tmp/preview.html

# Auto-open in browser
python -m scripts.render_wechat path/to/article.md --open
```

Output: a single `.html` file next to the article (or at `-o` path).

## Supported Markdown

| Element | Rendered as |
|---|---|
| `# ## ###` | h1 / h2 / h3 with inline style |
| `**bold**` | `<strong>` with accent color |
| `*italic*` / `_italic_` | `<em>` |
| `` `code` `` | `<code>` with muted background |
| ` ``` code block ``` ` | `<pre>` with dark theme |
| `- item` / `1. item` | `<ul>` / `<ol>` |
| `> quote` | `<blockquote>` |
| `[text](url)` | styled anchor |
| `![alt](src)` | responsive image |
| `---` | `<hr>` |

HTML is escaped inside code blocks and inline code. Paragraphs are
auto-joined across soft line breaks.

## Infographic Blocks (`:::type`)

For structured content (comparisons, hierarchies, flows, nested structures),
write an `:::type` fence block with a JSON body. The renderer produces a
styled HTML card using inline styles and `<table>` layout — same WeChat
safety guarantees as prose.

Why this matters: image generators can't spell. HTML/CSS cards guarantee
100% text accuracy, zero cost, and let you edit a number without regenerating
anything. An LLM in Phase 5 can emit these blocks based on the article's
structure.

### Four block types

**`:::comparison`** — 2–3 side-by-side cards for contrasting concepts:

```
:::comparison
{
  "title": "两种开头，同一个话题",
  "columns": [
    {"label": "差的开头", "content": "自古以来，拖延症就是困扰人类的难题。", "note": "教科书体", "color": "orange"},
    {"label": "好的开头", "content": "昨晚我又看了 3 小时短视频。", "note": "具体场景", "color": "blue"}
  ]
}
:::
```

**`:::pyramid`** — horizontal tiered cards with increasing saturation:

```
:::pyramid
{
  "title": "读者注意力的三层",
  "subtitle": "从划走边缘到深度阅读",
  "levels": [
    {"label": "标题级", "content": "扫一眼决定点不点", "tag": "5 秒", "color": "green"},
    {"label": "首屏级", "content": "前 200 字决定看不看完", "tag": "30 秒", "color": "amber"},
    {"label": "深读级", "content": "全文读完 + 转发", "tag": "3-10 分钟", "color": "blue"}
  ],
  "footnote": "每层流失 70%"
}
:::
```

**`:::flowchart`** — N horizontal nodes with arrows between each:

```
:::flowchart
{
  "title": "一篇文章的完整流水线",
  "subtitle": "从想法到可发布的稿子",
  "nodes": [
    {"label": "1. 拆解想法", "content": "一句话复述\n+ 2-3 角度", "note": "选方向", "color": "blue"},
    {"label": "2. 调研素材", "content": "事实 · 案例\n反面观点", "note": "装弹药", "color": "orange"},
    {"label": "3. 写初稿", "content": "场景开头\n观点推进", "note": "不说教", "color": "amber"},
    {"label": "4. 审查修订", "content": "事实核查\n多角度审", "note": "防翻车", "color": "green"}
  ]
}
:::
```

**`:::nested`** — concentric boxes for recursive/structural metaphors:

```
:::nested
{
  "title": "函数调用的嵌套结构",
  "layers": [
    {"text": "输出结果", "color": "blue"},
    {"text": "组合数据", "color": "orange"},
    {"text": "获取原始数据", "color": "green"}
  ],
  "footnote": "内层先算，结果喂给外层"
}
:::
```

### Palette names

Shared across all block types: `blue` (default), `orange`, `green`, `amber`,
`purple`, `rose`, `slate`. Using the same palette names across blocks in one
article keeps the visual system coherent.

### Error handling

A malformed JSON body or unknown block type renders as a red dashed error
card with the raw payload shown — the article render never aborts. Check
the output to find and fix the broken block.

### LLM authoring prompt

Hand this to Claude during Phase 5 to get blocks auto-inserted:

> Read the article. Identify paragraphs that are essentially comparisons,
> hierarchies, sequential processes, or nested structures. For each,
> replace with a `:::comparison` / `:::pyramid` / `:::flowchart` /
> `:::nested` block using the article's exact words as labels and
> content. Keep existing prose before and after. Don't invent data.

## Integration with the Writer Workflow

This script is meant to run at the **end of Phase 5 (platform formatting)**
when the target platform is WeChat.

Recommended flow inside Phase 5:

1. Take the stage-4-revised markdown as input
2. Apply WeChat-specific copy edits (short paragraphs, bolded keywords,
   title ≤ 30 chars, added summary line)
3. Save the polished markdown as `<slug>-wechat.md`
4. Run `python -m scripts.render_wechat <slug>-wechat.md --open`
5. Tell the user: "Open the HTML, click 『一键复制正文』, paste into WeChat
   editor. Preview on both desktop and mobile before publishing."

### Suggested addition to SKILL.md Phase 5

```markdown
**For WeChat**: after generating the WeChat-style markdown, render it to a
copy-paste-ready HTML preview:

    python -m scripts.render_wechat <article>-wechat.md --open

This produces a single HTML file with a one-click copy button. Copy the
article body, paste into the WeChat editor — styles survive the paste.
```

## Design Notes

- **Why table layout instead of flex/grid**: WeChat's mobile client on
  older Android WebViews sometimes renders flex children stacked; tables
  are the lowest-common-denominator that works everywhere.
- **Why inline styles only**: the WeChat editor's HTML sanitizer strips
  `class` and any `<style>` tags. Rich output must carry its CSS per node.
- **Why a separate copy area**: the toolbar uses `position: sticky` and
  `onclick` handlers that don't belong in the final post. Wrapping the
  article in a `<section id="copyArea">` and scripting
  `range.selectNode(copyArea)` ensures only the body is copied.
- **Dependency-free**: uses Python stdlib only (`re`, `html`, `argparse`,
  `pathlib`). No markdown parser needed because the subset above covers
  what the writer workflow produces.

## Limitations

- Tables (markdown `|...|` syntax) are not currently supported. If needed,
  add a table parser and render with `<table style>` + per-cell inline
  styles.
- Nested lists are flattened at one level. Acceptable for WeChat-style
  articles where deep nesting hurts mobile readability anyway.
- Images are passed through as-is. For WeChat uploads, host images on a
  CDN the editor can fetch, or replace with local paths after paste.
