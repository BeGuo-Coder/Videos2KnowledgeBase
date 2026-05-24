# Social Video Transcriber

一个 Claude Skill：把社交平台短视频/图文链接（抖音、B 站、小红书、YouTube、TikTok、快手、微博…）解析成结构化的 Markdown 内容报告，并维护一份 Obsidian 「视频内容总表」知识库。

适合自媒体运营者、研究者、知识库爱好者：每天看到一个值得拆解的视频，丢给 Claude 一条 URL，自动产出去水印链接、转写正文、提取关键词、判断可复用价值，并按主题（自媒体选题 / 个人形象 / 情感知识库 / 学术研究 …）归档进 Obsidian。

---

## ⚠️ 关于 API / 服务的声明（请先读）

本仓库**仅提供 Skill 提示词与脚本**，不提供也不代发任何商用/付费 API。运行本 Skill 需要你自行准备以下两类外部服务：

1. **去水印解析接口** (`SOCIAL_VIDEO_PARSER_BASE_URL`)
   - 仓库不内置任何解析地址。
   - 你可以自建（如开源项目 `Douyin_TikTok_Download_API`、`yt-dlp` 二次封装等），或采购商用 API。
   - 兼容条件：GET 请求，URL 末尾以 `url=` 结尾，原视频 URL 作为查询参数附加；响应优先 JSON。
   - 若不接入解析接口，B 站 / 抖音可直接走仓库内的 `yt-dlp` fallback 流程。

2. **语音转写服务** (`DASHSCOPE_API_KEY`)
   - 默认走阿里云百炼 / DashScope 的 `paraformer-v2`，你需要自行申请：<https://bailian.console.aliyun.com/>
   - 也可以替换为本地 ASR（如 `faster-whisper`），见 `references/bilibili-ytdlp-asr.md` 的本地 ASR 段落。

> **作者使用的是某第三方中转服务来获取上游模型/接口能力，不在此公开推荐，也不为任何第三方服务的可用性、合规性、安全性背书。**
> **请自行调研选择 — 任何 API key、付费、合规风险由使用者自行承担。**

`.env.example` 中的所有 key 都需要你自己填入。仓库不附带任何示例密钥。

---

## ✨ 核心能力

- **去水印解析**：调用你配置的解析接口拿到无水印媒体地址 + 元信息。
- **语音转写**：阿里云百炼 / DashScope ASR（`paraformer-v2`）把音视频转成正文，可替换为本地 ASR。
- **小红书图文笔记**：自动下载 `pics` → 拼接 contact sheet → 视觉 OCR → 重写成结构化报告。
- **学术帖溯源**：识别 arXiv/DOI 类内容，抓原始论文 PDF，产出含 task breakdown + research roadmap 的研究向笔记。
- **多级 fallback**：抖音解析空响应 → `yt-dlp --dump-json` → ASR；ASR 失败 → 帧拼接 + 视觉 OCR；B 站优先 `yt-dlp` + 官方字幕 API。
- **Obsidian 知识库联动**：自动按内容类型分流到不同 vault 子目录，并在「视频内容总表.md」追加/更新一行索引。
- **价值判断维度**：每条视频会被打上「知识库积累 / 二创素材 / 反面案例 / 仅归档」+ 风险备注，避免把灰色流量内容当成正向模仿对象。

## 📁 目录结构

```
social-video-transcriber/
├── SKILL.md                          # Skill 主提示词（Claude 读这个）
├── README.md                         # 本文件
├── .env.example                      # 环境变量模板（复制为 .env.local 后填值）
├── agents/
│   └── openai.yaml                   # Agent metadata
├── scripts/
│   └── parse_and_transcribe.py       # 解析 + ASR + Markdown 生成主脚本
└── references/                       # 进阶/兜底工作流文档
    ├── academic-social-note-workflow.md
    ├── bilibili-ytdlp-asr.md
    ├── configuration.md
    ├── douyin-ytdlp-fallback.md
    ├── douyin-ytdlp-ocr-fallback.md
    ├── hermes-local-env.md
    ├── relationship-gray-traffic.md
    ├── video-knowledge-table.md
    ├── xiaohongshu-html-state-fallback.md
    └── xiaohongshu-image-notes.md
```

## 🚀 安装

### 1. 放进 Claude Skills 目录

把整个 `social-video-transcriber/` 文件夹放到：

- **Claude Code 个人级**：`~/.claude/skills/social-video-transcriber/`
- **Claude Code 项目级**：`<project>/.claude/skills/social-video-transcriber/`
- **Hermes**：`<your_hermes_root>/.hermes/skills/media/social-video-transcriber/`

### 2. 安装 Python 依赖

```bash
pip install requests dashscope
# 可选：抖音/B 站 fallback
pip install yt-dlp
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env.local`（与 `SKILL.md` 同级），填入你自己的密钥：

```bash
cp .env.example .env.local
```

需要的变量：

| 变量 | 必需 | 说明 |
|---|---|---|
| `DASHSCOPE_API_KEY` | ✅ (用 DashScope 时) | 阿里云百炼 / DashScope API Key，需自行[申请](https://bailian.console.aliyun.com/) |
| `SOCIAL_VIDEO_PARSER_BASE_URL` | ⭕ | 你自己的去水印解析接口前缀，必须以 `url=` 结尾；不填则只能走 yt-dlp 兜底 |
| `DASHSCOPE_ASR_MODEL` | ⭕ | 默认 `paraformer-v2` |
| `SOCIAL_VIDEO_OUTPUT_DIR` | ⭕ | Markdown 报告输出目录，建议指向你的 Obsidian vault 子目录 |

### 4. 按你的 vault 结构调整 SKILL.md

`SKILL.md` 和 `references/` 中所有路径都使用 `<your_vault_root>` 占位符。你可以：

- 把占位符替换为你自己的 vault 绝对路径，或者
- 让 Claude 在对话中按你的 vault 实际结构动态决定输出位置。

仓库内提到的子目录（`自媒体选题库/`、`情感知识库/`、`个人形象管理/`）是作者使用的分类示例，**仅作参考，请按你自己的知识库组织方式调整**。

## 💬 使用

把视频链接发给 Claude，触发词例如：

- "解析一下这个视频 https://v.douyin.com/xxx/"
- "把这条小红书图文转成笔记"
- "更新一下我的视频内容总表"
- "提取核心做成图发我"（会走 baoyu-infographic 流程）

Claude 会自动调用 `scripts/parse_and_transcribe.py`：

```bash
python scripts/parse_and_transcribe.py "https://example.com/video" --output report.md
```

## 📊 输出示例

每条视频会产出两份产物：

1. **详细报告**（Markdown）：基本信息表 + 转写正文 + 关键词 + 备注
2. **总表索引行**：

```markdown
| 日期 | 平台 | 标题/主题 | 内容类型 | 核心观点 | 可复用价值 | 风险/备注 | 原文链接 | 解析笔记 |
```

## 🧩 与其他 Skill 协作

- `baoyu-infographic`：当用户要求"做成图"时，Claude 会先调用本 Skill 出报告，再交给信息图 Skill 出图。
- `arxiv` / `read-arxiv-paper`：当社交帖讲论文时，链式调取原始 PDF 做 ground truth 验证。
- `obsidian` / note-taking：写入 vault 时遵守 wikilink 风格。

## ⚖️ 伦理与边界

- 仅处理公开内容，不绕过付费墙、登录墙、私密内容、风控。
- 自动给灰色流量 / PUA / 焦虑营销内容打"反面案例"标签，不鼓励正向模仿。
- API Key 永不写进报告/日志。
- 遵守各平台的服务条款、版权与机器人协议。

## 📜 License

MIT

## 🙏 致谢

- 阿里云百炼 / DashScope —— ASR 能力
- yt-dlp —— 兜底下载
- Anthropic Claude Skills —— 提示词框架

## 免责声明

本仓库为个人学习与知识管理工具，按"AS IS"提供。
- 不保证任何 API、解析接口、转写服务的可用性。
- 不为任何第三方服务的合规性、安全性、计费方式背书。
- 使用本 Skill 处理的内容请遵守所在国家/地区法律与目标平台的服务协议。
- 由使用本仓库代码导致的任何直接或间接损失，作者不承担责任。
