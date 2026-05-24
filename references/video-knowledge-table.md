# Video Knowledge Table Reference

Use this reference when maintaining the Obsidian short-video knowledge base.

## Default location

```text
<your_vault_root>/自媒体选题库/视频内容总表.md
```

Detailed reports usually live in:

```text
<your_vault_root>/自媒体选题库/视频解析报告/
```

> Replace `<your_vault_root>` with your own Obsidian vault path. The Chinese folder name `自媒体选题库` is an example category; adapt to match your vault organization.

## Default table schema

```markdown
| 日期 | 平台 | 标题/主题 | 内容类型 | 核心观点 | 可复用价值 | 风险/备注 | 原文链接 | 解析笔记 |
|---|---|---|---|---|---|---|---|---|
```

## Row template

```markdown
| YYYY-MM-DD | 抖音 | 标题/主题 | 内容类型 | 一句话核心观点 | 高/中/低：适合哪个账号，为什么 | 风险或备注 | 原始链接 | [[视频解析报告/笔记名]] |
```

## Classification hints

### 内容类型 examples

- `AI 工具 / Agent 工作流`
- `科研方法 / 论文阅读`
- `保研辅导 / 面试 SOP`
- `AI 商业化 / 本地商家`
- `生活技能 / 标准答案型教程`
- `男性情感 / 灰色流量案例`
- `解析失败`

### 可复用价值 examples

Use `可复用价值` as a decision label, not a forced 二创 judgment. Many videos should be saved only as searchable knowledge.

- `知识库积累：用于以后查阅 AI Agent 产品趋势，暂不需要二创。`
- `知识库积累：保存为"标准答案型教程"结构样本，后续需要时再迁移。`
- `二创素材：适合论文创新账号，能改成"研二如何低成本找创新点"。`
- `二创素材：适合 AI 本地商家账号，能改成"越缺客户越容易吓跑客户"。`
- `反面案例：只适合拆灰色流量结构，不建议正向模仿。`
- `仅归档：信息密度不足，暂时无明确用途。`

### 风险/备注 examples

- `部分事实需要二次核验。`
- `价值观风险高：物化/操控/灰色营销。`
- `解析失败：需要完整分享文案、真实 video 链接或视频文件。`
- `ASR 可能有错字，引用前需人工校对。`

## Update workflow

1. Parse/transcribe video and write the detailed report.
2. Read or create `视频内容总表.md`.
3. Search for the video ID or original URL to avoid duplicates.
4. Append or replace one row with concise, decision-useful content.
5. Verify that the wikilink target matches the detailed note filename without `.md`.

## Suggested account-matrix axes

Replace these with your own account positioning. Common axes worth prioritizing extraction for:

1. 学习/考试辅导类账号（保研、考研、留学等）
2. AI/工具赋能行业类账号（如本地商家、教育、医疗）
3. 论文/学术/科研效率类账号
4. 个人成长/效率/方法论类账号
5. 反面案例：灰色流量、PUA、焦虑营销、私域转化（用于拆结构，不正向模仿）
