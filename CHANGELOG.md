# Changelog

> 格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，遵循语义化版本。

## [1.6.0] - 2026-04-22

**主题**:补 v1.5 的漏——Strict Mode 下 block 不该被主动弃用,要有使用规则。

### 背景

v1.5 Strict Mode 发布后测试发现,Claude 写稿时会"过度解读" Strict = 纯散文,主动弃用 HTML 信息图 block。但 Strict Mode 原本只禁小标题,没禁 block。结果用户失去了 writer-skill 最核心的差异化卖点(block 配图),换来的只是 khazix 化的纯散文。这是规则没写清导致的副作用。

v1.6 把 "Strict 下 block 怎么用" 明写出来,避免 Claude 再主动放弃。

### 新增

- **SKILL.md 新增 "Visual Blocks in Strict Mode" 小节**
  - 明确:Strict Mode 下 block 仍允许,是 writer-skill 的核心差异化,不能丢
  - 硬上限:Strict 下 ≤ 2 张(默认 3-4)
  - 类型优先级:pyramid > flowchart > comparison > nested
  - 强制散文包裹:每张 block 前后必须有口语转场句
  - block 内容纪律:footnote 必须口语化,tag 要有判断性不能是中性标签
  - **Block 省略测试**:加 block 前自问"如果不画,三段散文能不能讲清楚",能就不加

- **Phase 5 节更新**:
  - 候选清单生成时 Strict Mode 降到 ≤ 2 张
  - 插入时必须做"散文包裹"处理
  - 类型优先级明写进 Phase 5 流程

- **L3-8 Block 有机性检查(新)**
  - 每张 block 必须前有转场后有拾起
  - footnote 口语化扫描
  - tag 判断性扫描
  - Strict Mode 数量和类型双重校验

### 修复

- Strict Mode 下 Claude 的"配图恐慌"——把"不用小标题"错误泛化为"不用任何视觉元素"
- 自检报告格式加 L3-8 条目
- **[严重 bug 修复] 英文标点混入中文正文**——v1.4/v1.5 下 Claude 写的所有文章中文正文逗号都是 ASCII `,` 而不是中文 `，`(实测 v1.5 有 232 处英文逗号、0 处中文逗号)。这是极强的 AI tell——一眼翻译感
  - 根因:Claude 的 tokenizer 把 ASCII 标点训练进了中文上下文,默认输出就是半角
  - 解决:新增 L1-6 全角标点检查(默认开,不是 opt-in)+ 新脚本 `scripts/fix_punct.py` 一键批量修
  - 脚本规则:行 CJK 占比 ≥ 30% → 视为中文句子,所有非代码非 URL 非小数点的英文标点替换成全角

### 新增脚本

- **`scripts/fix_punct.py`** —— 全角标点自动修复工具
  - 用法:`python3 -m scripts.fix_punct <article>.md [--dry-run]`
  - 保护:代码块 / `:::block` JSON / markdown 链接 URL / 小数点 / 纯英文行
  - Phase 5 渲染前建议自动跑一次

### 设计取舍

- **为什么不把 block 在 Strict Mode 下直接禁掉**:writer-skill 最大的技术差异就是 HTML block,禁了就只剩下 khazix 的复制品。价值反而消失
- **为什么用"散文包裹"规则而不是"简单限量"**:数量限制解决不了"块感"问题。真正的问题是 block 和散文的衔接姿态——block 应该像"聊到这里顺手在餐巾纸上画一下",不是"插入一张卡片"
- **为什么类型优先级 pyramid > comparison**:pyramid 视觉上更像"从上到下一条线"的思考轨迹,comparison 的双列卡片读起来最像"AI 做的表格"。Strict 追求人味就要避开后者

---

## [1.5.0] - 2026-04-22

**主题**：借鉴 khazix-writer 的强规则，补"AI 味"这条 writer-skill 一直没根除的薄弱环节。

### 背景

对比测试发现，writer-skill 默认模式下产出依然有明显 AI 味，而 khazix-writer 的输出人味显著更强。拆解后定位到 4 条机械差别：禁标点 / 口语词硬下限 / 小标题纪律 / 文化升维 + 回环呼应强制。本次把这些嫁接进来，但做成 **opt-in 开关** 不影响攻略和技术 PM 稿子。

### 新增

- **Strict Human Voice Mode** —— EXTEND.md 新字段 `human_voice_strict: true` 开启
  - `L1-5` 禁标点扫描：冒号 `:`、破折号 `——`、双引号 `""` 全禁（改用 `「」` 或无引号）
  - `L2-3` 口语词下限从 ≥5 提到 **≥8** distinct phrases
  - `L2-5` 小标题纪律：思辨文/随笔/评论默认纯散文，用口语转场替代 `##`（攻略不受影响）
  - `L3-6` 文化升维硬要求：至少一处把具体话题连到更大的文化/历史/文学参照物
  - `L3-7` 回环呼应硬要求（契诃夫之枪）：开头埋的元素结尾必须 callback
  - Voice & Style 节新增 Phase 3 写稿行为要求：**原生按 Strict 模式写，不是写完再改**

- **chinese_casual_phrases.md 词库扩充**
  - 情绪类：加「给我一下子整不会了」「你敢信」「这种感觉太爽了」「我真的被震撼到了」
  - 口癖类：加「这玩意儿」「不是哥们」「这尼玛就是」「我寻思了一下我没寻思明白」「太特么 X 了」

- **EXTEND.md.example** 对应更新

### 设计取舍

- **为什么做成 opt-in 不做成默认**：攻略和技术文章需要小标题、冒号、结构化清单，把 Strict 规则强加会让这类文章变差。opt-in 让用户按文章类型选
- **为什么 Strict 下 Phase 3 要"原生写"不是"写完再改"**：后期修补会留残迹（句子结构已按带冒号破折号的方式搭好，拆只会让句子破碎）。第一遍按规则写会得到根本不同的句子架构
- **为什么要文化升维和回环呼应而不只是标点规则**：标点规则砍 AI 格式特征，升维+呼应加"这是一个作品不是一堆信息"的质感。两个方向都要动

### 哪些不动

- 6 Phase 工作流 / Auto Plan Mode / Core Values / HTML 信息图 DSL / 角色自动发现 / run_review.py 真并行
- 所有非 Strict 场景行为完全保持 v1.4 一致

---

## [1.4.0] - 2026-04-22

**主题**：借鉴 khazix-skills 的最佳实践，补齐 skill 的自审、边界、定位三大短板。

### 新增

- **四层自检体系（L1-L4）** —— 独立的自审协议（L1 硬性规则扫描 / L2 风格一致性 / L3 内容深度 / L4 活人感终审），每层有明确 pass/fail 标准
  - Auto Plan Mode 下**取代 Phase 6 的 6 角色模拟**（更机械可靠，无自评分偏高问题）
  - 交互模式下作为 Phase 6 的预检机制
  - 用户可通过"帮我快速自审一下"单独触发
- **`references/positioning_patterns.md`** —— 5 种定位（思辨文/攻略/随笔/评论/翻译）的完整写作骨架
  - 每种定位列出：适用场景、默认参数、结构 shape、写作重心、常见失败模式
  - Phase 3 写稿时按匹配 pattern 组织结构
  - 附 khazix 5 种原型（调查实验/产品体验/现象解读/工具分享/方法论分享）到本 5 定位的映射
- **"What AI Can and Can't Do" 节**（SKILL.md）—— AI 能力边界明写
  - ✅ AI 擅长：找证据 / 找类比 / 按确定角度扩写 / 学科背景 / 结构建议
  - ❌ AI 必须不做：第一手观察 / 核心创意角度 / 真实感受 / 价值判断 / 用户私人踩坑
  - Phase 3 遇到需要 AI-must-not-do 内容时，自动标 `[TODO]` 而非编造；有 `[TODO]` 时 Auto Plan Mode Hard Block
- **"Core Values" 节**（SKILL.md 开头）—— 4 条最高原则作为规则冲突的 tiebreaker
  - 讲人话 > 教科书话
  - 判断 > 模糊
  - 诚实 > 完整
  - 具体 > 抽象
- **`references/chinese_casual_phrases.md`** —— 默认中文口语词库（转场/判断/自嘲/情绪/拉近 5 类），给没配 `preferred_phrases` 的新用户"活人感底色"
- **`disable_default_casual_phrases` 字段**（EXTEND.md） —— 学术风/冷峻风用户可完全关闭默认词库
- **description 触发词扩充**（SKILL.md frontmatter） —— 列 10+ 个自然触发语 + 明确"不用于"清单，提升 agent 激活率

### 变更

- Auto Plan Mode 的 Phase 6 ReAct 自审从"6 角色模拟"改为"四层自检（L1-L4）"，更可靠
- SKILL.md 从 686 行增至 ~900 行（加 Core Values / AI 能力边界 / 四层自检三节）

---

## [1.3.0] - 2026-04-22

**主题**：从 human-in-the-loop 升级到可选 ReAct agent。

### 新增

- **Auto Plan Mode**（取代旧 Quick Mode）
  - Plan-first：Skill 先给完整执行计划（定位/角度/调研/配图/审查/交付），用户 approve 一次
  - 一口气跑完 Phase 2-6，中间不打断
  - Hard Block 条件明列：只在事实错误 ❌ / 关键素材缺失 / block 渲染失败 / source-auditor 🚨 / 定位中途不匹配 时才回来问
  - ReAct 自审协议：每个 Phase 结束 skill 跑 self-audit checklist，不合格就自己迭代
  - 触发：`--auto` / "自动跑" / "一把梭" / EXTEND.md 的 `quick_mode_default: true`
- **Language Convention 节**写进 SKILL.md，明确 5 类文件的语言规则（指令英文/角色中文/用户接口中文/代码英文）
- **Claude Code Plan Mode 兼容声明**：明说 Phase 3-6 在 plan mode 下不能落盘，建议退出再跑

### 变更

- `quick_mode_default` 字段语义更新：从"跳过 Phase 1/2 确认"→"默认进 Auto Plan Mode"。字段名保留不变（向后兼容）

### 修复

- 删除 Progress Indicator 部分对 "Quick Mode" 的遗留引用

---

## [1.2.0]

**主题**：从通用写作 → 吃用户私人素材 + 素材使用审计。

### 新增

- **`content_sources` 字段**（EXTEND.md）—— 用户本地学习笔记、踩坑本、项目日志作为 Phase 2 一手素材库
  - 优先级：`content_sources` > WebSearch > 通用知识
  - 防止"作者有独特材料但没用 → 文章浅"的问题
  - 和 `style_samples`（风格参考）分离：content = 说什么，style = 怎么说
- **第 6 个审查角色：`source-auditor`**（素材审计师）
  - 专查文章对 content_sources 的使用率、血泪 vs 通用占比、元洞察引用
  - 使用率 < 40% 触发 🚨 红旗
  - 只在有 content_sources 时跑，否则自动跳过
- **来源标签机制**（Phase 2）—— 每条 finding 强制标 `[一手/二手/转述/推断]`
  - Phase 4 核查优先验 `[转述]` 和 `[推断]`，减少幻觉
- **文章定位系统**（Phase 1）—— 5 种定位自动分配默认参数
  - 思辨文 1500-2500 / 攻略 3000-4500 / 随笔 800-1500 / 评论 800-1500 / 翻译 匹配原文
  - 每种定位对应不同字数和配图密度
  - 中途改定位协议：用户说"要攻略不是思辨文"→ 重新协商字数和配图
- **Phase 6 模拟 vs 真实并行偏差声明**—— 明写"单对话模拟版评分系统性偏高"，推荐高 stakes 用 `run_review.py` 真并行
- **示范 prompt 抒情化约束**（Voice & Style 节）—— 明确"Demo prompts 的评判标准是'能不能复制走跑'，不是'读起来美不美'"
- **pyramid 能力评估用法**（info-architect.md）—— 支持 `AI ✓ / AI ✗` 标签，适合讲能力边界的文章

### 变更

- Phase 6 reviewer 从 5 个变 6 个（新增 source-auditor），自动发现机制不变
- EXTEND.md.example + references/EXTEND.md.template 同步 content_sources 字段

---

## [1.1.0]

**主题**：从文字 skill → 带图 + 个性化的 skill。

### 新增

- **Phase 5: 配图** 独立成一个 Phase（原来藏在 Phase 4 子步骤）
  - 4 种信息图 block DSL：`:::comparison` / `:::pyramid` / `:::flowchart` / `:::nested`
  - Python 渲染器（`scripts/infographics.py`）用 inline style + table 布局，微信公众号兼容
  - **不用图像模型**：HTML 信息图文字 100% 精准、像素级对齐、改 JSON 字段就重渲染
- **微信 HTML 渲染器**（`scripts/render_wechat.py`）
  - markdown → 自包含 HTML，一键复制按钮
  - table 布局不用 flex/grid，微信编辑器粘贴后格式零损失
- **EXTEND.md 个性化机制**
  - 用户级 / 项目级两档配置
  - `target_reader` / `style_samples` / `banned_phrases` / `preferred_phrases` / `default_platform` / `default_word_count`
  - 首次使用温和询问（3 个可选问题），可跳过、可落盘
- **审查角色自动发现**—— `roles/*.md` 自动识别为 reviewer
  - BUILDER_ROLES 常量排除非审查角色（如 info-architect）
  - 新增角色无需改 Python 代码
- **`roles/info-architect.md`** —— Phase 5 专用 builder 角色，识别结构段插入 block
- **Phase 1 HOT/WARM/COLD 三路径**—— 根据输入信号数（主题/素材/类型）分配不同上手流程
  - HOT：跳过复述和提问，直接给候选角度
  - WARM：一句复述 + 一个问题 + 候选角度
  - COLD：完整 restate + 3 sharp questions

### 变更

- 从 5 Phase 流程升级到 6 Phase（拆分"核查+排版"为 Phase 4 核查、Phase 5 配图、Phase 6 审查）
- Phase 4 聚焦纯事实核查，Phase 5 独立承担视觉化主角
- `config` 目录重组为 `references/`

---

## [1.0.0]

### 核心能力

- 5 Phase 工作流（解题 → 调研 → 写稿 → 核查+排版 → 审查）
- 5 个独立审查角色（读者 / 编辑 / 事实核查 / 文体教练 / 平台策略师）
- WebSearch 集成
- 多平台适配（公众号 / 知乎 / 小红书）
- eval 框架（with/without skill 对比测试）
- eval-viewer HTML 可视化

### 设计理念

- 审查和修改分离：5 角色只提问题不改稿，用户是最终判决者
- 事实错误例外：`fact-checker` 的 ❌ 标记强制修改

---

## 版本号约定

- **Major** (x.0.0)：流程结构变化（如 5 Phase → 6 Phase）
- **Minor** (1.x.0)：新增能力、新角色、新字段
- **Patch** (1.1.x)：bug 修复、文档校订，无功能变化
