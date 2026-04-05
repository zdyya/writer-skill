# Writer Skill for Claude Code

从一个碎片化的想法到可发布的文章 —— 一个完整的 AI 写作工作流技能。

```mermaid
graph LR
    A[💡 一个想法] --> B[🔍 搜索研究]
    B --> C[✍️ 写稿]
    C --> D[📋 事实核查 + 📱 平台排版]
    D --> E[👥 5角色并行审查]
    E --> F[✅ 终稿]
```

## 这是什么？

这是一个 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 的 Skill，安装后 Claude 会自动识别写作意图并启动完整工作流。

你只需要给一个想法（哪怕只是一句话），Skill 会引导 Claude 完成从灵感到终稿的全过程。

## 核心特性

### 5 阶段工作流

| 阶段 | 做什么 |
|---|---|
| **Phase 1: 拆解想法** | 理解你的灵感，提出角度，等你确认方向 |
| **Phase 2: 搜索研究** | 用 WebSearch 搜集事实、数据、案例、反面论证 |
| **Phase 3: 写稿** | 按口语化风格写完整文章，场景开头，不说教 |
| **Phase 4: 事实核查 + 交付** | 逐条核查文中每个事实声明，标记 ✅❌⚠️🔶 |
| **Phase 5: 多角色审查** | 5 个独立 AI 角色并行审查，交叉验证找出真问题 |

### 5 个独立审查角色

每个角色有专属的评分维度和输出格式，彼此看不到对方的审查结果：

| 角色 | 关注什么 |
|---|---|
| **读者** | 钩子、参与感、清晰度、情绪共鸣、转发欲 |
| **编辑** | 结构、节奏、用词、冗余、过渡 |
| **事实核查员** | 每一条数据、引用、人名、理论是否准确 |
| **文体教练** | 声音一致性、口语节奏、意象比喻、句式变化 |
| **平台策略师** | 标题力、首屏吸引力、平台适配、互动触发、转发机制 |

审查完成后生成汇总报告，标注**被多个角色同时指出的共识问题**（可信度最高）。

### 多平台适配

自动为不同平台生成对应格式的版本：

- **微信公众号**：30字内标题、短段落、加粗金句、图片位建议、评论区引导
- **知乎**：更多引用和论据、清晰的论证结构
- **小红书**：500-800字精简版、个人化语气、表情和标签建议

### 快速模式

不想来回确认？说"直接写"，Claude 会自动选角度、研究、写稿、核查，一步到位。

## 安装

```bash
# 克隆仓库并复制到 Claude Code skills 目录
git clone https://github.com/zdyya/writer-skill.git
cp -r writer-skill ~/.claude/skills/writer
```

只需要 `SKILL.md` 和 `roles/` 目录就能用。其余文件是开发工具，可选。

## 使用：写文章

安装后，直接跟 Claude 说你的想法：

```
"帮我写篇文章，聊聊为什么现代人越来越喜欢独处"
"我有个想法，AI 会不会取代程序员？写篇公众号文章"
"直接帮我写一篇关于拖延症的文章，发知乎和小红书"
"写完了，帮我审查一下"
```

Claude 会自动识别意图并启动对应的工作流。**不需要跑任何脚本**，整个流程在对话中自动完成。

### 流程中每个文件的角色

| 阶段 | Claude 做什么 | 用到的文件 |
|---|---|---|
| Phase 1: 拆解想法 | 理解你的灵感，提出角度 | `SKILL.md` |
| Phase 2: 搜索研究 | 用 WebSearch 搜集事实和数据 | `SKILL.md` |
| Phase 3: 写稿 | 按口语化风格写完整文章 | `SKILL.md` |
| Phase 4: 事实核查 | 逐条核查文中的事实声明 | `SKILL.md` |
| Phase 5: 多角色审查 | 5 个 AI 角色并行审查文章 | `SKILL.md` + `roles/*.md` |

> **你只需要 `SKILL.md` + `roles/` 目录。** Claude 读取这些文件后，用自身的内置工具（WebSearch、Agent 等）跑完全流程。

---

## 使用：开发与测试 Skill

> 以下工具是给**想改进这个 Skill 的开发者**用的。写文章不需要。

如果你 fork 了这个项目想优化 prompt，需要一种方式验证"改完之后效果是不是变好了"。这就是以下脚本的用途。

### 第一步：跑对比测试

```bash
cd ~/.claude/skills/writer
python3 -m scripts.run_eval --workspace /path/to/workspace
```

读取 `evals/evals.json` 里的测试用例，每个用例跑两遍：
- **有 Skill**：带着 SKILL.md 生成文章
- **没 Skill**：裸跑同一个 prompt

输出保存在 workspace 目录，方便对比。

### 第二步：查看对比结果

```bash
python3 eval-viewer/generate_review.py /path/to/workspace --skill-name writer
```

启动浏览器界面（默认 `localhost:3117`），可视化对比 with/without skill 的输出，支持在线打分和反馈。

### 第三步（可选）：命令行批量审查

```bash
python3 -m scripts.run_review /path/to/article.md --output-dir /path/to/reviews
```

不进对话，直接在命令行跑 5 个角色并行审查。适合批量处理或 CI 集成。

### 各文件说明

| 文件 | 用途 |
|---|---|
| `scripts/run_eval.py` | 测试运行器 — 跑 with/without skill 对比 |
| `scripts/run_review.py` | 命令行版多角色审查 — 用 `claude -p` 启动 5 个并行进程 |
| `scripts/utils.py` | 共享工具函数 — 解析 SKILL.md、处理环境变量等 |
| `scripts/__init__.py` | Python 包标记文件（空的） |
| `evals/evals.json` | 4 个测试用例 — 包含 prompt、期望输出、评估维度 |
| `agents/grader.md` | 评分 agent — 测试跑完后自动评判输出质量 |
| `eval-viewer/generate_review.py` | 启动 HTML 可视化界面 |
| `eval-viewer/viewer.html` | 可视化模板 — 展示对比结果 |

---

## 输出样例

不想看文档？直接看效果：

- [**文章：全民蒸馏时代**](examples/article-distill-your-ex.md) — 从"如果能把前任蒸馏成AI"这个想法出发，聊 MBTI、标签化社交、AI 思维入侵人际关系
- [**多角色审查报告**](examples/review-summary.md) — 5 个独立 AI 角色对这篇文章的并行审查结果

以上由 Writer Skill 的完整工作流自动生成。

## 目录结构

```
writer/
│
│  📝 写文章用的（核心）
├── SKILL.md                    # 主技能定义，驱动整个写作流程
├── roles/                      # 5 个审查角色 prompt（Phase 5 用）
│   ├── reader.md               #   读者 — 钩子、参与感、转发欲
│   ├── editor.md               #   编辑 — 结构、节奏、用词
│   ├── fact-checker.md         #   事实核查员 — 数据、引用准确性
│   ├── style-coach.md          #   文体教练 — 口语节奏、意象
│   └── strategist.md           #   平台策略师 — 标题力、平台适配
│
│  📄 输出样例
├── examples/
│   ├── article-distill-your-ex.md  #   示例文章：全民蒸馏时代
│   └── review-summary.md          #   示例审查报告
│
│  🔧 改进 Skill 用的（开发/测试）
├── scripts/                    # Python 脚本
│   ├── run_eval.py             #   with/without skill 对比测试
│   ├── run_review.py           #   命令行批量审查
│   ├── utils.py                #   共享工具函数
│   └── __init__.py             #   Python 包标记
├── evals/
│   └── evals.json              #   测试用例（4 个）
├── agents/
│   └── grader.md               #   测试评分 agent
└── eval-viewer/
    ├── generate_review.py      #   启动可视化界面
    └── viewer.html             #   HTML 模板
```

## 设计理念

### 为什么不让 AI 自己改自己的文章？

早期版本让 Claude 写完文章后自己审查、自己修改。测试发现这会导致文章越改越"安全"——个性被磨平，变成标准学术腔。

原因是同一个模型的审美权重是固定的：它写作时回避的风格，审查时也会标记为"问题"，修改时自然会进一步回避。循环几轮后，文章趋于平庸。

**解决方案：审查和修改分离。** 5 个角色只负责提出问题，不动手改。最终由用户决定改什么、不改什么。事实错误除外——那个必须改。

### 为什么需要 5 个角色？

单一视角容易有盲点。5 个角色从完全不同的维度审查同一篇文章，**被多个角色同时指出的问题**可信度最高（交叉验证）。这比一个"全能审查员"给出的反馈更有参考价值。

## 目标读者画像

- 年轻、好奇心强
- 兴趣横跨文学、历史、哲学、心理学、AI、互联网
- 注意力短但愿意为好内容停留
- 转发能让自己显得有趣的文章

## 语言

文章风格为**口语化中文**——像一个聪明朋友跟你聊天，不像教科书在讲课。

## 关于这个项目

这个 Skill 是我和 Claude Code 一起共创的。整个开发过程本身就是一次 AI 协作实验：

- Claude 负责写代码、写 prompt、跑测试
- 我负责提需求、审结果、做判断
- 我们一起发现了"AI 自审自改会把文章改差"的问题，并设计了多角色独立审查的解决方案

如果你对 Claude Code Skills 的开发感兴趣，欢迎参考这个项目的结构。有问题可以开 Issue。

## License

MIT
