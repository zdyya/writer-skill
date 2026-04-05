# Writer Skill for Claude Code

从一个碎片化的想法到可发布的文章 —— 一个完整的 AI 写作工作流技能。

## 这是什么？

这是一个 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 的 Skill，安装后 Claude 会自动识别写作意图并启动完整工作流：

**构思 → 搜索研究 → 写稿 → 事实核查 → 平台排版 → 多角色审查**

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

将 `writer/` 目录复制到你的 Claude Code skills 目录：

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/writer-skill.git

# 复制到 Claude Code skills 目录
cp -r writer-skill/writer ~/.claude/skills/writer
```

或者直接把整个仓库克隆到 skills 目录下。

## 使用

安装后，直接跟 Claude 说：

- "帮我写篇文章，聊聊为什么现代人越来越喜欢独处"
- "我有个想法，AI 会不会取代程序员？写篇公众号文章"
- "直接帮我写一篇关于拖延症的文章，发知乎和小红书"
- "写完了，帮我审查一下"

Claude 会自动识别意图并启动对应的工作流。

## 自带的脚本工具

Skill 内置了可独立运行的 Python 脚本（仅依赖标准库）：

### 多角色并行审查

```bash
cd ~/.claude/skills/writer
python3 -m scripts.run_review /path/to/article.md --output-dir /path/to/reviews
```

5 个角色并行跑 `claude -p`，自动汇总结果。

### 测试用例运行器

```bash
python3 -m scripts.run_eval --workspace /path/to/workspace
```

跑 `evals/evals.json` 中的测试用例，with/without skill 对比，验证 skill 是否有效。

### HTML 审查界面

```bash
python3 eval-viewer/generate_review.py /path/to/workspace --skill-name writer
```

启动浏览器界面，可视化对比测试结果，支持在线反馈。

## 目录结构

```
writer/
├── SKILL.md                    # 主技能定义
├── roles/                      # 5 个审查角色 prompt
│   ├── reader.md
│   ├── editor.md
│   ├── fact-checker.md
│   ├── style-coach.md
│   └── strategist.md
├── scripts/                    # Python 脚本
│   ├── utils.py
│   ├── run_review.py           # 多角色并行审查
│   └── run_eval.py             # 测试用例运行器
├── eval-viewer/                # HTML 审查界面
│   ├── generate_review.py
│   └── viewer.html
├── evals/
│   └── evals.json              # 测试用例
└── agents/
    └── grader.md               # 写作评分 agent
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
