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

- 🧠 **从一句话灵感到可发布 HTML 的全链路写作** —— 你给主题，它给你一篇可直接粘贴到公众号的成品（含配图）
- 🎨 **用 HTML 信息图替代图像模型** —— 4 种结构图（对比 / 层级 / 流程 / 嵌套），文字 100% 精准、改一个字不用重生图
- 📚 **吃你的私人素材** —— 学习笔记、踩坑本、项目日志都可以做成一手素材源，比 WebSearch 靠谱
- 🔍 **6 角色并行审查 + 四层自检** —— 审查和写作分离，不让 AI 自己给自己打高分
- 🙋 **按你的声音写** —— 用你过往文章锚定风格，避免写成"平均 AI 腔"
- 🏷️ **减少虚构** —— 每条 finding 强制分类 `[一手/二手/转述/推断]`，Phase 4 核查优先验靠不住的
- ⚡ **一键跑完模式** —— 给主题 + 批一次计划 → 自动跑完所有阶段，交付 HTML

---

## 一分钟上手

```bash
# 1. 安装
git clone https://github.com/zdyya/writer-skill.git ~/.claude/skills/writer

# 2. 可选：创建你的个人偏好（强烈推荐）
cp ~/.claude/skills/writer/.writer-skill/EXTEND.md.example ~/.writer-skill/EXTEND.md
# 用编辑器打开 ~/.writer-skill/EXTEND.md，写上你的读者、风格样本、禁用词
```

装完直接跟 Claude 说：

```
"帮我写一篇关于拖延症的文章"
"我有个想法：AI 会不会让人变笨？写篇公众号长文"
"帮我把这个会议纪要整理成文章"
```

Skill 自动识别写作意图，启动 6 阶段流程。**不需要跑任何脚本**。

不想来回确认的话，加 `--auto`：

```
"帮我写一篇关于 AI PM 面试踩坑的文章 --auto"
```

Skill 会先给你一份执行计划，你批一次，然后自动跑完所有阶段给你 HTML。

---

## 6 阶段工作流

每一阶段 Skill 都会告诉你"现在在哪、接下来是什么"，不会静默跑。

### Phase 1: 解题

你给一个主题（哪怕只是"AI 和心理学"这么简单），Skill 判断你的输入完整度，给 2-3 个候选角度让你选。每个角度会标注它最适合写成什么类型（思辨文 / 攻略 / 随笔 / 评论 / 翻译）和对应字数。

输入越模糊，它问得越细；输入越具体，问得越少。

### Phase 2: 调研

Skill 先读你的 content_sources（如果你配了的话——比如学习笔记或踩坑本），再用 WebSearch 补外部证据。最后给你一份调研简报，每条 finding 都标了来源可信度（`[一手] / [二手] / [转述] / [推断]`）。

### Phase 3: 初稿

按你选的角度、按定位对应的结构骨架写稿。如果 EXTEND.md 里有 `style_samples`，Skill 会先读你过往的文章模仿句式节奏。写完给你看，等你反馈。

如果稿子里需要你自己的真实经历但 content_sources 里没有，Skill 不会硬编——会明确标一个 `[TODO]` 让你填。

### Phase 4: 核查

WebSearch 逐条核查文中的事实声明。**不自动改稿**，只标记：
- ✅ 已核实
- ❌ 需更正（给出正确信息 + 来源）
- ⚠️ 无法核实
- 🔶 有误导性

改不改由你决定。

### Phase 5: 配图 🎨

Skill 扫全文，识别那些"本来就是结构化内容但用散文勉强表达"的段落——比如"三层""两种""四个步骤""A → B → C"这种。然后用 4 种 HTML 信息图 block 之一替代，让读者一眼看见结构。

配图不调图像模型（图像模型画信息图必有错字和对齐漂移），用 HTML + CSS 渲染，配色保证全文一致。最后跑出一个微信公众号兼容的单文件 HTML，带一键复制按钮。

### Phase 6: 审查

6 个独立 AI 角色并行审稿：

- **读者**：我刷到这篇会看完吗？
- **编辑**：结构、节奏、用词、冗余
- **事实核查员**：每条数据 / 引用 / 人名 / 日期
- **文体教练**：读起来像同一个人在说话吗？
- **平台策略师**：标题会被点开吗？哪里会劝退？
- **素材审计师**：你的踩坑本用到位了吗？（只在有 content_sources 时跑）

6 个角色互相看不见对方的结果。最后汇总哪些问题**被多个角色同时点中**——那些是最值得改的真问题。

---

## Auto Plan Mode（一键跑完）

每 Phase 都要用户确认太累？用 Auto Plan Mode：

1. 你给一个主题 + `--auto`
2. Skill 给你一份**执行计划**（定位 / 角度 / 调研源 / 字数 / 配图数 / 审查方式）
3. 你说 "ok" 批准一次
4. Skill 自动跑 Phase 2-6，**不来打扰**
5. 最后一次性给你所有产物

只在真正需要你判断的时候 Skill 才会打断你（事实错误、素材严重缺失、定位中途不匹配、配图失败）。

Auto Plan 下默认用**四层自检**（L1 禁用词扫描 / L2 风格一致性 / L3 内容深度 / L4 活人感终审）替代 6 角色模拟——更机械可靠，不会自评分偏高。

---

## 个性化（EXTEND.md）

默认情况下 Skill 按通用设置写作。如果你想按**你自己的声音**写，创建 `.writer-skill/EXTEND.md` 告诉 Skill：

- 🎯 你的目标读者是谁
- 📖 你过往写得最好的几篇文章路径（Skill 读完模仿你的声音）
- 📚 你的学习笔记 / 踩坑本放在哪（作为一手素材）
- 🚫 你讨厌哪些词（追加到默认禁用词上）
- 💬 你偏好的表达（会被自然穿插）
- 📱 默认发什么平台、字数多长

完整示例见 [`.writer-skill/EXTEND.md.example`](.writer-skill/EXTEND.md.example)。

**首次使用**：如果你没配这个文件，Skill 会在 Phase 1 开头温和地问一次（3 个可选问题），你可以跳过或随手填几个。填了之后 Skill 会问你要不要存成文件，下次直接用。

---

## 4 种信息图 block

Skill 在 Phase 5 会用以下 4 种之一来可视化结构段：

- **`:::comparison`** —— 2-3 列对比卡片（讲"两种东西" / "A vs B"时用）
- **`:::pyramid`** —— 3-5 层金字塔（讲"三层结构" / "从基础到高级"时用，也支持能力评估标签如 AI ✓ / AI ✗）
- **`:::flowchart`** —— N 节点流程（讲"第一步…第二步" / 因果链时用）
- **`:::nested`** —— 外层包内层的嵌套盒子（讲调用栈、嵌套关系时用）

所有 block 用 `<table>` + inline style 布局（微信公众号编辑器兼容，不用 flex/grid）。改一个字只要改 JSON 就重新渲染，不用重生图。

完整 DSL 手册见 [`scripts/RENDER_WECHAT.md`](scripts/RENDER_WECHAT.md)。

---

## 命令行工具（给开发者）

> 普通写作不需要这些。这些是给想改 Skill 的开发者用的。

- **`scripts/render_wechat.py`** —— markdown（含 `:::block`）→ 微信 HTML
- **`scripts/run_review.py`** —— 命令行起多个 claude -p 子进程并行跑所有 reviewer 角色，比对话里模拟真并行
- **`scripts/run_eval.py`** —— 用测试用例跑 with/without skill 对比
- **`eval-viewer/`** —— HTML 可视化界面

每个脚本自己的 `--help` 会列出参数。

---

## 设计理念

### 为什么不让 AI 自己改自己的文章？

早期版本让 Claude 写完后自己审查、自己修改。结果越改越"安全"——个性被磨平，变成标准学术腔。

同一个模型的审美权重是固定的：它写作时回避的风格，审查时也会标记为"问题"，修改时进一步回避。循环几轮后，文章趋于平庸。

**所以：审查和修改分离**。6 个角色只提问题，不动手改。用户是最终判决者。只有事实错误（❌）强制必改。

### 为什么信息图用 HTML 不用图像模型？

图像模型再强也只是"画得像字"——必然有错字、字号不稳、风格漂移。改一个数字要重生整张图。

HTML/CSS 画同样的图：文字 100% 精准、像素级对齐、改 JSON 字段就重渲染。唯一短板是不能画封面 / 氛围图 / 插画——但这些本来就不该 AI 自动生成。

### 为什么要有 Auto Plan Mode，同时保留默认 6 Phase？

写作有两种场景：**精打细磨**（一篇公众号头条，用户想全程参与）和 **批量产出**（周更随笔，用户只想要结果）。

默认 6 Phase 满足前者。Auto Plan Mode 作为**可选加速**满足后者。不是替代关系。

### 为什么 AI 必须不碰某些内容？

AI 写的骨架和连接组织是 OK 的，但**第一手观察、核心创意角度、真实情绪反应、用户私人踩坑故事**——这些 AI 一编就假。

Auto Plan Mode 在 Phase 3 遇到这种内容时会标 `[TODO]`，**不会硬编**一个"一次我用 X 遇到 Y"的假故事——这是 Skill 不越权的安全网。

---

## 目录结构

```
writer-skill/
├── SKILL.md                           # 主技能定义
├── roles/                             # 审查角色（自动发现）
│   ├── reader.md / editor.md / fact-checker.md
│   ├── style-coach.md / strategist.md
│   ├── source-auditor.md              # reviewer：素材使用审计
│   └── info-architect.md              # builder：Phase 5 配图识别
├── scripts/
│   ├── render_wechat.py               # markdown → 微信 HTML
│   ├── infographics.py                # 4 种 block 渲染
│   ├── run_review.py                  # 命令行批量审查
│   ├── run_eval.py                    # 对比测试
│   └── RENDER_WECHAT.md               # block DSL 手册
├── .writer-skill/
│   └── EXTEND.md.example              # 个性化配置入口
├── references/
│   ├── EXTEND.md.template             # 完整 schema
│   ├── positioning_patterns.md        # 5 种定位的写作骨架
│   └── chinese_casual_phrases.md      # 默认中文口语词库
├── examples/
│   ├── article-time-management.md     # 示例文章
│   ├── article-time-management.html   # 渲染后 HTML
│   └── review-summary.md              # 审查报告样例
├── evals/  agents/  eval-viewer/      # 测试 & 可视化
├── CHANGELOG.md
├── README.md
└── LICENSE                            # MIT
```

---

## Skill 自己的语言规则

这个 Skill 里的文件是中英混合的：
- **指令 / 规则**（SKILL.md, references/）用英文——对 LLM 指令精度更高
- **角色 prompt**（roles/）用中文——教 Claude 写中文用中文讲
- **用户接口**（README, EXTEND.md 模板, CHANGELOG）用中文——中文用户看得懂

---

## License

MIT
