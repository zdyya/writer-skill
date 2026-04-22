# Writer Skill for Claude Code

ChatGPT 写的稿子读起来像 PPT 模板：正确、全面、客气、没人想读。

你改了 3 遍 prompt，换了 3 个模型。AI 依然在那里兢兢业业地生产**"看上去像文章但读起来很 AI"** 的东西。

这个 Skill 是我做给自己的解药。

它不教你写更长的 prompt。它把一整套中文写作方法论**工程化**——从「怎么选角度」到「什么时候该用图」到「你自己的踩坑本怎么被用进文章」到「写完怎么自检不是 AI 腔」。

四个版本打磨到现在，做 6 件事：

- 🧠 **Auto Plan Mode** —— 给一个主题 + 批一次计划 → 自动跑完所有阶段交付 HTML
- 📚 **content_sources** —— 你的学习笔记 / 踩坑本当一手素材库，比 WebSearch 靠谱
- 🎨 **4 种 HTML 信息图 block** —— 用 DSL 替代图像模型，文字 100% 精准、改 JSON 就重渲
- 🔍 **6 角色审查 + L1-L4 四层自检** —— 审查和写作分离，不让 AI 自己给自己打高分
- 🏷️ **来源标签强制分类** —— `[一手/二手/转述/推断]`，减少虚构
- 🙋 **EXTEND.md 个性化** —— 用你过往文章锚定风格，让 AI 写出"你的腔调"不是"平均腔调"

这是一个 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 的 Skill。按下方「[安装](#安装)」安装后，跟 Claude 说"帮我写..."，自动启动完整流程。**不需要跑任何脚本**。

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

## 四个版本的演进主线

每个版本不是随意加功能，是真实踩坑之后补的：

| 版本 | 核心升级 | 背后的真实踩坑 |
|---|---|---|
| **v1.1** | 配图独立 Phase + HTML + 个性化 | 用图像模型配信息图，全是错字 → 意识到信息图本质是排版+文字，用 HTML |
| **v1.2** | content_sources + 素材审计师 | 写出来的东西"浅"，不是 AI 能力问题，是作者自己的独特素材没用进去 |
| **v1.3** | Auto Plan Mode + ReAct 自审 | 每 Phase 都要用户确认太累 → 给用户"批一次计划就跑到底"的选项 |
| **v1.4** | 四层自检 + AI 能力边界 + 5 种定位骨架 | Auto Plan Mode 的 6 角色模拟自评分偏高 → 换成机械的 L1-L4 + 明写 AI 能做什么不能做什么 |

## 核心特性

### 6 阶段工作流

| 阶段 | 做什么 |
|---|---|
| **Phase 1: 解题** | 识别输入温度 + 提出候选角度 + 自动定位（思辨文/攻略/随笔/评论/翻译） |
| **Phase 2: 调研** | 优先读 content_sources → 再 WebSearch。每条 finding 强制标 `[一手/二手/转述/推断]` |
| **Phase 3: 初稿** | 按口语化风格写完整文章，场景开头，不说教 |
| **Phase 4: 核查** | 逐条核查文中事实声明，标记 ✅❌⚠️🔶（不改稿，只标记） |
| **Phase 5: 配图** 🎨 | 识别结构段 → 插入 HTML 信息图 → 渲染成微信兼容 HTML |
| **Phase 6: 审查** | 6 个独立 AI 角色并行审查（含 source-auditor 专查素材使用率） |

---

### ⚡ Auto Plan Mode（v1.3 主卖点）

默认 6 Phase 流程每阶段都要用户确认 —— 适合精打细磨，但如果你想**一键出稿**，用 Auto Plan Mode。

**触发**：`--auto` / "自动跑" / "一把梭" / EXTEND.md 里 `quick_mode_default: true`

**流程**：

```
用户：写一篇关于 X 的文章 --auto
       ↓
Skill：📋 Execution Plan
       - 定位：思辨文
       - 角度：A（最锐）
       - 素材源：WebSearch + content_sources
       - 字数：1800
       - 配图：2 张 comparison + 1 张 pyramid  
       - 审查：跑 6 reviewer（并行）
       - 交付：markdown + HTML + review report
       → 说 "ok" 开始，或告诉我改哪项
       ↓
用户：ok
       ↓
Skill 自动跑 Phase 2-6（不打断你）
       ↓
最后一次性交付所有产物
```

**Hard Block 条件**（skill 唯一会打断你的时候）：
- Phase 4 发现 ❌ 事实错误
- Phase 5 block 渲染失败多次
- Phase 6 source-auditor 标红 🚨（严重低用素材）
- 关键素材缺失
- 定位中途不匹配

这把 skill 从 human-in-the-loop 变成了**可选的 ReAct agent**。Skill 用自审替代用户 observer，循环自己跑完。

---

### 🎨 Phase 5: 配图

这是 Skill 和普通 AI 写作工具的核心差异点。info-architect 角色扫全文，识别需要可视化的结构段，用 4 种 HTML 信息图 block 替代散文：

| Block | 用途 | 语言信号 |
|---|---|---|
| `:::comparison` | 2-3 列对比卡片 | "两种" "对比" "过去 vs 现在" |
| `:::pyramid` | 多层级结构 | "三层" "五个等级" |
| `:::flowchart` | N 节点流程 | "第一步…第二步" "A → B → C" |
| `:::nested` | 嵌套盒子 | "嵌套" "调用链" |

**为什么不用图像模型**：信息图的本质是"排版 + 精确文字"，图像模型再强也是"画得像字"，必然有错字、对齐漂移。HTML/CSS 画同样的图：文字 100% 精准、像素级对齐、改 JSON 就重渲染。

**特殊用法**：pyramid 支持"能力评估"标签（如 `AI ✓ · 可模仿` / `AI ✗ · 没有自己`），适合讲能力边界类文章。

### 🙋 个性化（EXTEND.md）

每个创作者都有自己的腔调，不希望 Claude 把文章写成"平均 AI 味儿"。

```yaml
version: 1

target_reader: |
  AI PM、创业者、产品思辨爱好者。讨厌 PPT 体和鸡汤。

# 风格参考：模仿句式节奏（纯风格，不抄内容）
style_samples:
  - /Users/you/writing/代表作.md

# 内容素材库：v1.2 新增，比 WebSearch 更靠谱
content_sources:
  - path: /Users/you/学习笔记/
    type: learning_notes
  - path: /Users/you/踩坑本.md
    type: war_stories

banned_phrases: [心智, 打法, 赛道]
preferred_phrases: [较劲, 落地, 踩过]

default_platform: wechat
auto_render_wechat: true
quick_mode_default: false  # 设 true 默认进 Auto Plan Mode
```

**首次使用**：Skill 检测到没有 EXTEND.md 时，**Phase 1 开头温和问一次**（3 个可选问题：风格参考 / 禁用词 / 平台+字数）。你可以跳过，之后不再问。

**style_samples vs content_sources**：
- `style_samples` = **声音**（怎么说）→ Phase 3 写稿前读
- `content_sources` = **内容**（说什么）→ Phase 2 调研时读

### 👥 审查角色（6 个，自动发现）

| 角色 | 类型 | 关注什么 |
|---|---|---|
| 读者 | reviewer | 钩子、参与感、转发欲 |
| 编辑 | reviewer | 结构、节奏、冗余 |
| 事实核查 | reviewer | 每条数据、引用、日期 |
| 文体教练 | reviewer | 声音、节奏、意象 |
| 平台策略师 | reviewer | 标题、平台适配、传播 |
| **素材审计师** | reviewer | **用户 content_sources 的使用率**（v1.2 新增） |
| 信息架构师 | builder | Phase 5 专用，识别结构段插信息图 |

- 加新 reviewer：把 `.md` 文件丢到 `roles/` 就自动注册
- **模拟 vs 真实并行的偏差**：在单对话里 Claude 扮 6 角时评分系统性偏高。`run_review.py` 起 6 个独立 subprocess 才是真并行

### 🏷️ 来源标签机制（v1.2 新增）

Phase 2 调研时，每条 finding 必须分类：

| 标签 | 含义 |
|---|---|
| `[一手]` | 原始来源（论文、官方声明、用户自己的材料） |
| `[二手]` | 靠谱转述（媒体报道、维基百科） |
| `[转述]` | 二手转述（"据说他说..."） |
| `[推断]` | 你自己的推断 |

Phase 4 核查时优先验 `[转述]` 和 `[推断]` —— 那是幻觉藏身的地方。

### 📝 文章定位（v1.2 新增）

每个候选角度自动标定位：

| 定位 | 默认字数 | 配图密度 | 场景 |
|---|---|---|---|
| 思辨文 | 1500-2500 | 2-3 张 | 一个核心判断 |
| 攻略 | 3000-4500 | 4-5 张 | 多层次教程 |
| 随笔 | 800-1500 | 0-1 张 | 个人化叙事 |
| 评论 | 800-1500 | 1-2 张 | 热点短评 |
| 翻译 | 匹配原文 | — | 译+轻注释 |

你可以中途改（"换成攻略"），skill 会重新协商字数和配图数。

### 多平台适配

- **微信公众号**：HTML + 一键复制（v1.1 增强）
- **知乎**：更多引用、清晰论证结构
- **小红书**：500-800 字精简版

## 安装

```bash
# 克隆仓库并复制到 Claude Code skills 目录
git clone https://github.com/zdyya/writer-skill.git
cp -r writer-skill ~/.claude/skills/writer

# 可选：创建个人偏好文件（强烈推荐）
cp ~/.claude/skills/writer/.writer-skill/EXTEND.md.example ~/.writer-skill/EXTEND.md
# 编辑 ~/.writer-skill/EXTEND.md 填你的读者、风格样本、content_sources、禁用词
```

核心只需要 `SKILL.md` + `roles/` + `scripts/render_wechat.py` + `scripts/infographics.py`。其余是开发工具，可选。

## 使用

### 写一篇文章

```
"帮我写一篇关于 AI 产品拟人的文章"
"写一篇讲远程工作效率的短评"
"基于我在 ~/notes/ 的笔记，写一篇关于时间管理的攻略"
```

Skill 自动识别主题、选定位、走 6 Phase。

### 一键跑完（Auto Plan Mode）

```
"帮我写一篇关于 AI 改变工作方式的文章 --auto"
"直接到底，主题是独立开发的焦虑"
```

Skill 给 Execution Plan → 你 approve → 自动跑完交付 HTML。

### 命令行批量审查

```bash
python3 -m scripts.run_review /path/to/article.md --output-dir /path/to/reviews
```

起 6 个 `claude -p` subprocess 并行跑所有 reviewer 角色。适合批量审查或 CI 集成。

### 单独跑 HTML 渲染

```bash
python3 -m scripts.render_wechat /path/to/article.md --open
```

把一篇带 `:::block` 的 markdown 渲染成微信公众号兼容 HTML。

## 设计理念

### 为什么不让 AI 自己改自己的文章？

早期版本让 Claude 写完后自己审查、自己修改。测试发现这会导致文章越改越"安全"——个性被磨平，变成标准学术腔。

原因是同一个模型的审美权重是固定的：它写作时回避的风格，审查时也会标记为"问题"，修改时自然进一步回避。循环几轮后，文章趋于平庸。

**解决方案：审查和修改分离。** 6 个角色只负责提出问题，不动手改。最终由用户决定改什么、不改什么。事实错误除外——那个必须改。

### 为什么需要 6 个审查角色？

单一视角容易有盲点。6 个角色从完全不同的维度审查同一篇文章，**被多个角色同时指出的问题**可信度最高（交叉验证）。第 6 个（素材审计师）是 v1.2 加的——专门抓"作者有独特素材但没用进文章"这个最高频的"文章浅"病因。

### 为什么配图要独立成 Phase 5？

早期把"生成信息图"放在 Phase 4 的子步骤里。这是错的。

信息图生成是**创造性工作**，和 Phase 3 写稿属于同一等级。把它降维成"排版附属"会让 Claude 敷衍——只插一两张图就完事。独立成 Phase 后，识别结构段 → 候选清单 → 用户确认 → 写 block → 渲染 HTML，每一步都有自己的舞台。

### 为什么信息图用 HTML 不用图像模型？

v1.1 之前试过图像模型方案：图像模型再强也只是"画得像字"，必然有错字、字号不稳、风格漂移；改一个数字要重生整张图，每张 ¥0.05 + 30 秒等待；不同图之间视觉风格漂移。

HTML/CSS 画同样的图：文字 100% 精准、像素级对齐、改 JSON 字段就重渲染、同一个 palette 保证全文一致。唯一短板是不能画氛围图 / 封面 / 插画 —— 但这类图本来就不该由 Skill 自动生成，手动做更合适。

### 为什么 v1.3 加 Auto Plan Mode？

前两个版本都是 human-in-the-loop —— 每个 Phase 用户确认一次。好处是精细，坏处是写一篇文章要做 10+ 个决策。对高频写作者是负担。

Auto Plan Mode 的核心洞察：**大多数决策可以在 Plan 里一次性约定**，剩下的由 skill 自审。只在真正需要人判断的时候（事实错误、素材严重缺失）才打断用户。这让 skill 从"工具型"升级到"代理型"。

但默认依然保留 6 Phase 交互流程 —— Auto Plan Mode 是**可选加速**，不是替代。

### 为什么语言规则要文档化？

这个 skill 本身是中英混合：SKILL.md 英文（LLM 指令精度），roles/*.md 中文（教 Claude 写中文），README 中文（给用户）。v1.3 把这个边界写进 SKILL.md 的 Language Convention 节，方便未来贡献者参考。

## 目录结构

```
writer-skill/
│  📝 核心（写文章用）
├── SKILL.md                           # 主技能定义（6 Phase + Auto Plan Mode）
├── roles/                             # 审查角色自动发现
│   ├── reader.md                      # 5 个 reviewer
│   ├── editor.md
│   ├── fact-checker.md
│   ├── style-coach.md
│   ├── strategist.md
│   ├── source-auditor.md              # v1.2 新增 reviewer：素材使用审计
│   └── info-architect.md              # builder：Phase 5 专用
├── scripts/
│   ├── render_wechat.py               # markdown → 微信 HTML
│   ├── infographics.py                # 4 种 block 渲染器
│   └── RENDER_WECHAT.md               # block DSL 手册
├── .writer-skill/
│   └── EXTEND.md.example              # 个性化配置模板
│
│  📄 输出样例
├── examples/
│   ├── article-time-management.md     # 示例文章：时间管理的三层
│   ├── article-time-management.html   # 渲染后的公众号 HTML
│   └── review-summary.md              # 审查报告示例
│
│  🔧 开发 / 测试
├── scripts/
│   ├── run_eval.py                    # with/without 对比测试
│   ├── run_review.py                  # 命令行批量审查（6 reviewer 并行）
│   └── utils.py
├── evals/evals.json                   # 测试用例
├── agents/grader.md                   # 测试评分 agent
└── eval-viewer/                       # HTML 可视化界面
```

## 目标读者画像

默认目标读者（可通过 EXTEND.md 的 `target_reader` 覆盖）：

- 年轻、好奇心强
- 兴趣横跨文学、历史、哲学、心理学、AI、互联网
- 注意力短但愿意为好内容停留
- 转发能让自己显得有趣的文章

## 语言

文章风格为**口语化中文**——像一个聪明朋友跟你聊天，不像教科书在讲课。

Skill 本身的文档用英文（指令精度），roles 用中文（教 Claude 写中文），面向用户的 README 和 EXTEND 模板用中文。详细规则见 SKILL.md 的 Language Convention 节。

## 关于这个项目

这个 Skill 是我和 Claude Code 一起共创的。整个开发过程本身就是一次 AI 协作实验：Claude 负责写代码、写 prompt、跑测试；我负责提需求、审结果、做判断。

**v1.0 的发现**是反直觉的：让 Claude 自审自改会把文章越改越平庸，于是设计了"独立审查 + 用户决定"的机制。

**v1.1 的起点**是一次踩坑：试着用图像模型给自己的文章配信息图，效果到处是小瑕疵。意识到信息图的本质是排版+精确文字，应该用 HTML。

**v1.2 的起点**是测试时发现：写出来的东西"浅"，不是 AI 写作能力问题，是**作者自己的独特素材没用进文章**。于是加了 content_sources 和 source-auditor。

**v1.3 的起点**是用户反馈：每 Phase 都要确认太累。Auto Plan Mode 让 skill 从工具型变成代理型 —— 你批一次计划，它跑到底。

写作工具的演进不只是"AI 代笔"，也不是"AI 代画"，而是让 AI 准确识别每种内容该用什么形式承载，以及让用户灵活选择"我要多少参与感"。Writer Skill 是我们在这个方向上的一次探索。

如果你对 Claude Code Skills 的开发感兴趣，欢迎参考这个项目的结构。有问题可以开 Issue。

## License

MIT
