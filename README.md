# Writer Skill for Claude Code

ChatGPT 写的稿子读起来像 PPT 模板：正确、全面、客气、没人想读。

你改了 3 遍 prompt，换了 3 个模型。AI 依然在那里兢兢业业地生产**"看上去像文章但读起来很 AI"** 的东西。

这个 Skill 是我做给自己的解药。它不教你写更长的 prompt，而是把一整套中文写作方法论**工程化**——从「怎么选角度」到「什么时候该用图」到「你自己的踩坑本怎么被用进文章」到「写完怎么自检不是 AI 腔」。

```mermaid
graph LR
    A[💡 一个想法] --> B[🔍 搜索研究]
    B --> C[✍️ 写稿]
    C --> D[📋 事实核查]
    D --> E[📊 配图<br/>信息图 + HTML]
    E --> F[👥 多角色审查]
    F --> G[✅ 终稿·可发布]
    style E fill:#2563EB,stroke:#1E40AF,color:#fff
```

## 能做什么

- 🧠 **从一句话灵感到可发布 HTML 的全链路写作** —— 你给主题，它给你一篇可直接粘贴到微信公众号的成品（含配图）
- 🎨 **用 HTML 信息图替代图像模型** —— 4 种结构块（对比 / 层级 / 流程 / 嵌套），文字 100% 精准、改 JSON 就重渲
- 📚 **吃你的私人素材** —— 学习笔记 / 踩坑本 / 项目日志都可以作为一手素材源，比 WebSearch 靠谱
- 🔍 **6 角色并行审查 + L1-L4 四层自检** —— 审查和写作分离，机械扫描 + 深度点评双保险
- 🙋 **按你的声音写** —— EXTEND.md 让你用过往文章锚定风格，避免写成"平均 AI 腔"
- 🏷️ **来源标签强制分类** —— 每条 finding 标 `[一手/二手/转述/推断]`，减少虚构
- ⚡ **一键跑完模式（Auto Plan Mode）** —— 给主题 + 批一次计划 → 自动跑完 6 Phase 交付 HTML

---

## 一分钟上手

### 安装

```bash
# 克隆仓库到 Claude Code skills 目录
git clone https://github.com/zdyya/writer-skill.git ~/.claude/skills/writer

# 可选：创建个人偏好文件
cp ~/.claude/skills/writer/.writer-skill/EXTEND.md.example ~/.writer-skill/EXTEND.md
# 编辑 ~/.writer-skill/EXTEND.md，填你的读者、风格样本、content_sources、禁用词
```

### 第一次调用

在 Claude Code / OpenClaw / Codex 里直接说：

```
帮我写一篇关于 [话题] 的文章
```

Skill 自动识别写作意图，启动 6 Phase 流程。**不需要跑任何脚本**。

### 一键跑完（Auto Plan Mode）

```
帮我写一篇关于 [话题] 的文章 --auto
```

Skill 给一份执行计划，你 approve 一次，它一口气跑完所有阶段交付 HTML。

---

## 6 Phase 工作流详解

每 Phase 有明确的 input / action / output。默认交互模式下每 Phase 结束等用户确认；Auto Plan Mode 下自动推进。

### Phase 1: 解题（Unpack the Idea）

| 字段 | 说明 |
|---|---|
| **Input** | 用户的初始输入（任何长度、任何完整度） |
| **Action** | 识别输入温度（HOT / WARM / COLD）→ 自动判断**文章定位**（思辨文 / 攻略 / 随笔 / 评论 / 翻译）→ 提出 2-3 个候选角度 |
| **Output** | 候选角度清单，每个带工作标题 + 一句话钩子 + 定位标注 |
| **Exit** | 用户必须选一个角度（或提出自己的）才能进 Phase 2 |

**输入温度分类**：

- **HOT**（主题 + 素材 + 类型齐全）：跳过复述和提问，直接给候选角度
- **WARM**（2/3 信号）：一句复述 + 一个针对缺失信号的问题 + 候选角度
- **COLD**（仅片段或灵感）：完整流程——复述 + 3 尖锐问题 + 候选角度

### Phase 2: 调研（Research & Gather Material）

| 字段 | 说明 |
|---|---|
| **Input** | 用户选定的角度 |
| **Action** | 优先读 content_sources（如配置）→ 再 WebSearch 补充外部证据 |
| **Output** | 调研简报：5-8 条 findings（每条带 `[一手/二手/转述/推断]` 标签）+ 1-2 个意外发现 + 反方观点 + 建议叙事结构 |
| **Exit** | 用户确认方向或调整 |

**来源标签**：

| 标签 | 含义 |
|---|---|
| `[一手]` | 原始来源验证过（论文、官方声明、用户 content_sources） |
| `[二手]` | 可靠的二次报道（主流媒体、维基百科） |
| `[转述]` | 二手转述（"据说他说..."） |
| `[推断]` | 作者自己的推断，未有直接来源 |

Phase 4 核查时会优先验 `[转述]` 和 `[推断]` —— 那是幻觉藏身的地方。

### Phase 3: 初稿（Draft）

| 字段 | 说明 |
|---|---|
| **Input** | 调研 findings + 选定角度 + EXTEND.md 配置 |
| **Action** | 按定位对应的结构骨架写稿（见 `references/positioning_patterns.md`），引用 style_samples 的声音节奏 |
| **Output** | 完整初稿（markdown） |
| **Exit** | 展示初稿，等用户修改意见 |

**定位对应的默认参数**：

| 定位 | 默认字数 | 结构重心 |
|---|---|---|
| 思辨文 | 1500-2500 | 钩子 → 反直觉判断 → 机制 → 反方 → 留余味结尾 |
| 攻略 | 3000-4500 | 痛点 → 框架 → 逐层展开（每层带 actionable）→ 整合 → 清单 |
| 随笔 | 800-1500 | 具体时刻 → 感受 → 文化升维 → 返回具体 |
| 评论 | 800-1500 | 事件 → 第一反应 → 深度分析 → 锐判断 → 短 kicker |
| 翻译 | 匹配原文 | 译者注 → 翻译 + 译注 → 简短 afterword |

### Phase 4: 核查（Fact Check）

| 字段 | 说明 |
|---|---|
| **Input** | Phase 3 初稿 |
| **Action** | 用 WebSearch 逐条核查文中事实声明（数据、引用、日期） |
| **Output** | 核查报告，每条标 `✅ 已核实 / ❌ 需更正 / ⚠️ 无法核实 / 🔶 有误导性` |
| **Exit** | 有 ❌ 时提示用户，但**不自动改稿**—— 用户决定 |

### Phase 5: 配图（Illustration）🎨

| 字段 | 说明 |
|---|---|
| **Input** | 初稿 + 选定平台 |
| **Action** | info-architect 角色扫文识别结构段 → 提候选 block 清单 → 用户确认 → 写 JSON → 渲染 HTML |
| **Output** | `<slug>-wechat.md`（含 `:::block`） + `<slug>-wechat.html`（浏览器可打开，含一键复制按钮） |
| **Exit** | 提示进入 Phase 6 审查 |

**微信 HTML 特点**：
- `<table>` + inline style 布局（不用 flex/grid，微信编辑器兼容）
- 一键复制按钮只在浏览器有效，不会进微信
- 粘贴到公众号编辑器后格式零损失

### Phase 6: 审查（Multi-Role Review）

| 字段 | 说明 |
|---|---|
| **Input** | Phase 5 的带图终稿 |
| **Action** | 6 个独立 reviewer 并行审（见下方「审查角色」节） |
| **Output** | 汇总报告：每角色评分表 + 共识问题 + 具体改稿建议 |
| **Exit** | **不自动改稿**——用户决定改什么 |

---

## Auto Plan Mode（一键跑完）

适合不想每 Phase 都确认的场景。

### 触发

- 用户说 `--auto` / "自动跑" / "一把梭" / "直接到底"
- 或 EXTEND.md 里 `quick_mode_default: true`

### 流程

```
用户：帮我写一篇关于 X 的文章 --auto
       ↓
Skill：📋 Execution Plan
       - 定位：<思辨文 | 攻略 | ...>
       - 角度：<具体角度 + 一句话理由>
       - 素材源：<WebSearch / content_sources 文件列表>
       - 字数：<默认或从 EXTEND.md>
       - 配图：<数量 + 类型>
       - 审查：<reviewer 列表 + 模式>
       - 交付：<markdown / HTML / review 报告>
       → 等用户说 "ok" 或 "改某项"
       ↓
用户：ok
       ↓
Skill 自动跑 Phase 2-6（不打断）
       ↓
一次性交付所有产物
```

### Hard Block 条件（skill 唯一会打断你的时候）

| 条件 | 为什么打断 |
|---|---|
| Phase 4 发现 ❌ 事实错误 | 用户必须决定改还是接受 |
| Phase 5 block 渲染失败 2 次以上 | 降级到无配图模式需确认 |
| 关键素材完全缺失（angle 依赖但找不到证据） | 角度可能不可行 |
| 定位中途不匹配（比如发现应该写攻略而不是思辨文） | 字数 / 配图密度需要重新协商 |
| Phase 3 有 `[TODO]` 未填（AI 标记需要用户自己的真实经历） | 不能编造，必须用户填 |

---

## EXTEND.md 配置接口

放在 `<项目>/.writer-skill/EXTEND.md`（项目级） 或 `~/.writer-skill/EXTEND.md`（用户级）。**项目级优先**。

### 完整 schema

```yaml
version: 1

# ─ 读者和声音 ─────────────────────

# 目标读者画像（覆盖默认）
target_reader: |
  自然语言描述，越具体越好

# 风格锚定样本：写稿前 skill 读这些文件模仿句式节奏（纯风格，不抄内容）
style_samples:
  - /absolute/path/to/best-article-1.md
  - /absolute/path/to/best-article-2.md

# 内容素材库：你的学习笔记 / 踩坑本 / 项目日志（一手素材优先于 WebSearch）
content_sources:
  - path: /absolute/path/to/notes/
    type: learning_notes    # learning_notes | war_stories | reference
  - path: /absolute/path/to/war-stories.md
    type: war_stories

# ─ 词汇偏好 ─────────────────────

# 禁用词（追加到默认禁用列表）
banned_phrases:
  - 心智
  - 打法
  - 赛道

# 偏好用词（自然穿插，不硬塞）
preferred_phrases:
  - 踩过
  - 落地
  - 较劲

# 是否关闭默认中文口语词库（references/chinese_casual_phrases.md）
disable_default_casual_phrases: false

# ─ 工作流偏好 ─────────────────────

# 默认发布平台
default_platform: wechat      # wechat | zhihu | xiaohongshu | substack

# 默认字数范围
default_word_count: [1500, 2500]

# 是否默认进 Auto Plan Mode
quick_mode_default: false

# Phase 5 结束时是否自动跑 render_wechat.py
auto_render_wechat: true
```

### 首次使用

如果没有 EXTEND.md，skill 在 Phase 1 会**温和问一次**（3 个可选问题：风格参考 / 禁用词 / 默认平台），你可以跳过。填了之后可以选择存成文件。

详见 [`.writer-skill/EXTEND.md.example`](.writer-skill/EXTEND.md.example)（最小可用版）和 [`references/EXTEND.md.template`](references/EXTEND.md.template)（完整 schema）。

---

## 信息图 Block DSL

在 markdown 里用 `:::type { JSON } :::` 嵌入信息图。渲染后是 HTML 卡片，微信编辑器兼容。

### 4 种 block

#### `:::comparison` — 2-3 列对比卡片

```
:::comparison
{
  "title": "标题",
  "subtitle": "副标题（可选）",
  "columns": [
    {"label": "左", "content": "主体内容", "note": "底注", "color": "blue"},
    {"label": "右", "content": "主体内容", "note": "底注", "color": "orange"}
  ],
  "footnote": "底部小字"
}
:::
```

**适用**：两种东西的并置（A vs B / 过去 vs 现在）。

#### `:::pyramid` — 多层级结构

```
:::pyramid
{
  "title": "标题",
  "subtitle": "副标题",
  "levels": [
    {"label": "浅层", "content": "说明", "tag": "标签", "color": "green"},
    {"label": "中层", "content": "说明", "tag": "标签", "color": "amber"},
    {"label": "深层", "content": "说明", "tag": "标签", "color": "blue"}
  ],
  "footnote": "底注"
}
:::
```

**适用**：3-5 层递进（浅到深 / 基础到高级）。支持**能力评估标签**（如 `AI ✓ · 可模仿` / `AI ✗ · 不可模仿`）。

#### `:::flowchart` — N 节点流程

```
:::flowchart
{
  "title": "标题",
  "subtitle": "副标题",
  "nodes": [
    {"label": "步骤 1", "content": "主内容", "note": "说明", "color": "blue"},
    {"label": "步骤 2", "content": "主内容", "note": "说明", "color": "orange"},
    {"label": "步骤 3", "content": "主内容", "note": "说明", "color": "green"}
  ],
  "footnote": "底注"
}
:::
```

**适用**：N 个有序步骤或因果链（3-5 个节点最佳）。

#### `:::nested` — 嵌套盒子

```
:::nested
{
  "title": "标题",
  "subtitle": "副标题",
  "layers": [
    {"text": "外层", "color": "blue"},
    {"text": "中层", "color": "orange"},
    {"text": "内层", "color": "green"}
  ],
  "footnote": "底注"
}
:::
```

**适用**：嵌套结构（调用栈 / 嵌套括号 / 组织层级）。layers 从外到内。

### 配色（Palette）

所有 block 共享 7 色调板：

| 名称 | 色调 |
|---|---|
| `blue` | 深蓝（冷 / 科技） |
| `orange` | 橙（暖 / 警示） |
| `green` | 绿（自然 / 开始） |
| `amber` | 琥珀（中间层） |
| `purple` | 紫（神秘 / 第三层） |
| `rose` | 玫红（强调） |
| `slate` | 灰（中性） |

详细 DSL 规则和错误兜底见 [`scripts/RENDER_WECHAT.md`](scripts/RENDER_WECHAT.md)。

---

## 6 个审查角色

放在 `roles/` 下，`scripts/run_review.py` 自动发现。

| 角色 | 关注维度 | 输出形式 |
|---|---|---|
| **读者**（reader） | 钩子 / 参与感 / 清晰度 / 情绪共鸣 / 转发欲 | 5 维 1-10 分 + 具体段落观察 |
| **编辑**（editor） | 结构 / 节奏 / 用词 / 冗余 / 过渡 | 5 维 1-10 分 + 可操作修改建议 |
| **事实核查员**（fact-checker） | 数据 / 引用 / 人名 / 日期 / 理论 | 每条事实 ✅/❌/⚠️/🔶 标记 |
| **文体教练**（style-coach） | 声音一致性 / 口语节奏 / 意象 / 首尾呼应 / 句式变化 | 5 维 1-10 分 + 具体改写示范 |
| **平台策略师**（strategist） | 标题力 / 首屏吸引力 / 平台适配 / 互动触发 / 转发机制 | 5 维 1-10 分 + 平台特定建议 |
| **素材审计师**（source-auditor） | content_sources 使用率 / 血泪占比 / 元洞察引用 | 使用率 % + 漏用的 missed opportunity 清单 |

**关键设计**：审查和修改分离。6 角色只提问题，**不动手改稿**。事实错误除外。

**自动发现**：`roles/*.md` 自动识别为 reviewer。要加新角色，写个 `.md` 文件丢进 `roles/` 就行，不用改代码。builder 类型（如 info-architect）在 `scripts/run_review.py` 的 `BUILDER_ROLES` 常量里登记。

---

## 四层自检（L1-L4）

Auto Plan Mode 下取代 Phase 6 多角色模拟（模拟自评分偏高），也可用户手动触发（"帮我快速自审一下"）。

| 层 | 检查内容 | Pass 标准 |
|---|---|---|
| **L1 硬性规则** | 禁用词扫描 / 结构套话 / 空泛工具名 / `[TODO]` 标记 | 零命中 |
| **L2 风格一致性** | 开头类型 / 节奏（长短句）/ 口语化密度 / 段落长度 | L2-1 必过 + 其他 3/4 通过 |
| **L3 内容深度** | 观点支撑 / 知识输出方式 / content_sources 使用率 / 反方观点 / 定位专项 | L3-1 + L3-2 必过，其他按适用性 |
| **L4 活人感终审** | 温度 / 独特性 / 姿态 / 心流 | 整体"像人写的"感觉 |

详见 SKILL.md 的 "Four-Layer Self-Audit Protocol" 节。

---

## 命令行接口

### render_wechat.py

```bash
python -m scripts.render_wechat <article.md> [--output FILE] [--open]
```

把一篇 markdown（可带 `:::block`） 渲染成微信兼容 HTML。

| 参数 | 说明 |
|---|---|
| `<article.md>` | 输入 markdown 文件路径 |
| `-o, --output` | 输出 HTML 路径（默认 `<article>.html`） |
| `--open` | 在浏览器自动打开 |

### run_review.py

```bash
python -m scripts.run_review <article.md> [--output-dir DIR] [--roles list] [--model MODEL] [--workers N]
```

起 N 个 `claude -p` 子进程并行跑所有 reviewer 角色（真实并行，比对话模拟评分更可靠）。

| 参数 | 说明 |
|---|---|
| `<article.md>` | 待审查的 markdown 文件 |
| `-o, --output-dir` | 审查报告输出目录（默认和文章同目录） |
| `--roles` | 指定跑哪些角色（默认跑所有 reviewer，排除 builder） |
| `--model` | 模型覆盖 |
| `--workers` | 并行 worker 数（默认 5） |

### run_eval.py

```bash
python -m scripts.run_eval --workspace /path/to/workspace
```

跑 `evals/evals.json` 里的测试用例，每个用例带 skill / 不带 skill 各跑一遍，生成对比数据。

---

## 目录结构

```
writer-skill/
│  📝 核心（写文章用）
├── SKILL.md                           # 主技能定义（6 Phase + Auto Plan Mode + 四层自检）
├── roles/                             # 审查角色（自动发现）
│   ├── reader.md / editor.md / fact-checker.md
│   ├── style-coach.md / strategist.md
│   ├── source-auditor.md              # reviewer：素材使用审计
│   └── info-architect.md              # builder：Phase 5 专用
├── scripts/
│   ├── render_wechat.py               # markdown → 微信 HTML
│   ├── infographics.py                # 4 种 block 渲染器
│   └── RENDER_WECHAT.md               # block DSL 完整手册
├── .writer-skill/
│   └── EXTEND.md.example              # 个性化配置入口
├── references/
│   ├── EXTEND.md.template             # 完整 schema 文档
│   ├── positioning_patterns.md        # 5 种定位的写作骨架
│   └── chinese_casual_phrases.md      # 默认中文口语词库
│
│  📄 输出样例
├── examples/
│   ├── article-time-management.md     # 示例文章：时间管理的三层
│   ├── article-time-management.html   # 渲染后的公众号 HTML
│   └── review-summary.md              # 审查报告示例
│
│  🔧 开发 / 测试
├── scripts/
│   ├── run_eval.py                    # with/without skill 对比测试
│   ├── run_review.py                  # 命令行批量审查
│   └── utils.py
├── evals/evals.json                   # 测试用例
├── agents/grader.md                   # 测试评分 agent
└── eval-viewer/                       # HTML 可视化界面
```

---

## 设计理念

### 为什么不让 AI 自己改自己的文章？

早期版本让 Claude 写完后自己审查、自己修改。测试发现这会导致文章越改越"安全"——个性被磨平，变成标准学术腔。同一个模型的审美权重是固定的：它写作时回避的风格，审查时也会标记为"问题"，修改时进一步回避。循环几轮后，文章趋于平庸。

**解决方案：审查和修改分离。** 6 角色只提问题，不动手改。用户是最终判决者。只有事实错误（❌）强制必改。

### 为什么信息图用 HTML 不用图像模型？

图像模型再强也只是"画得像字"——必然有错字、字号不稳、风格漂移。改一个数字要重生整张图，每张 ¥0.05 + 30 秒等待。

HTML/CSS 画同样的图：文字 100% 精准、像素级对齐、改 JSON 字段就重渲染、同一个 palette 保证全文一致。唯一短板是"不能画氛围图 / 封面 / 插画"——但这类图本来就不该由 Skill 自动生成。

### 为什么 Auto Plan Mode 保留默认 6 Phase 不替代？

写作有两种场景：
- **精打细磨**（一篇公众号头条）：用户想全程参与，每 Phase 确认
- **批量产出**（周更的随笔、工作稿子）：用户只想要结果

默认保留 6 Phase 满足前者。Auto Plan Mode 作为**可选加速**满足后者。不是替代关系。

### 为什么 AI 必须不碰某些内容？

见 SKILL.md 的 "What AI Can and Can't Do" 节。核心判断是——**AI 写的骨架和连接组织，用户供血**。第一手观察、核心创意角度、真实情绪反应、用户私人踩坑故事——这些 AI 一编就假。Auto Plan Mode 在 Phase 3 遇到这种内容时会标 `[TODO]`，不会硬编一个"一次我用 X 遇到 Y"的假故事。

---

## Language Convention

Skill 内部文档是中英混合的。看文件或贡献代码前参考这个规则：

| 文件类型 | 语言 | 为什么 |
|---|---|---|
| 指令 / 规则 / 结构（SKILL.md, references/） | 英文 | LLM 指令精度更高 |
| Role prompts（roles/） | 中文 | 教 Claude 写中文用中文 |
| 用户接口文本（exit prompts, 样例短语） | 中文 | 终端用户看得懂 |
| README / EXTEND.md 模板 / CHANGELOG | 中文 | 用户文档 |
| 代码 + 代码注释 | 英文 | 标准实践 |

---

## License

MIT
