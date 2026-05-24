---
name: social-video-transcriber
description: parse and transcribe social video links into markdown reports and maintain an Obsidian short-video knowledge base table. use when the user provides a douyin, bilibili, youtube, xiaohongshu, tiktok, kuaishou, weibo, or similar short-video/social-media URL and asks to parse, remove watermark, transcribe, summarize, extract content, update the table/知识库, or produce a content report. this skill uses a configured parser endpoint/yt-dlp fallback and dashscope speech recognition, then saves both a detailed note and a row in the video content index table when the vault path is available.
---

# Social Video Transcriber

## Overview

Use this skill to turn a single social-video URL into a Markdown content report. The default pipeline is:

1. Call the no-watermark parser endpoint with the original URL.
2. Extract the best video/audio URL plus metadata from the parser response.
3. Transcribe the media through Alibaba Cloud Bailian / DashScope ASR.
4. Produce a clean Markdown report with platform, title, author, publish time, content, and keywords/tags.

Respect platform terms, copyright, and user authorization. Do not help bypass paywalls, private content, login-only content, or access controls.

## Required configuration

### Hermes local install note

When installed as a Hermes skill, prefer a skill-local `.env.local` so gateway/WeChat runs do not depend on shell exports. Put it next to `SKILL.md`:

```text
<skill_dir>/.env.local
```

Recommended keys:

```bash
DASHSCOPE_API_KEY="your_api_key"
DASHSCOPE_ASR_MODEL="paraformer-v2"
SOCIAL_VIDEO_OUTPUT_DIR="<your_vault_root>/自媒体选题库/视频解析报告"
```

If the bundled script does not load `.env.local`, add a tiny bootstrap near the top of `scripts/parse_and_transcribe.py` that reads `KEY=VALUE` lines from `.env` and `.env.local` without overwriting existing process environment variables. This avoids requiring `/restart` or global shell exports for every gateway run.

### Parser and ASR config

The no-watermark parser base URL must be provided via environment variable (no default bundled):

```text
SOCIAL_VIDEO_PARSER_BASE_URL="<your_parser_endpoint_ending_with_url=>"
```

For ASR, require the user environment to provide a Bailian/DashScope API key:

```bash
export DASHSCOPE_API_KEY="your_api_key"
```

Optional environment variables:

```bash
export SOCIAL_VIDEO_PARSER_BASE_URL="custom_parser_prefix_ending_with_url="
export DASHSCOPE_ASR_MODEL="paraformer-v2"
export SOCIAL_VIDEO_OUTPUT_DIR="/absolute/path/to/output"
```

Never print API keys or include them in reports.

## Obsidian knowledge-base workflow

When the user sends a public social-video link for parsing, create/update two artifacts whenever possible:

1. A detailed Markdown report under:
   `<your_vault_root>/自媒体选题库/视频解析报告/`
2. A summary row in the table note:
   `<your_vault_root>/自媒体选题库/视频内容总表.md`

> Replace `<your_vault_root>` with your own Obsidian vault path. The Chinese folder names below (`自媒体选题库`, `情感知识库`, `个人形象管理`) are example categories — adjust to match your own knowledge-base structure.

The table row should capture the video's practical value at a glance, not just metadata. Use these columns by default:

```markdown
| 日期 | 平台 | 标题/主题 | 内容类型 | 核心观点 | 可复用价值 | 风险/备注 | 原文链接 | 解析笔记 |
```

For `可复用价值`, do not force every item into 二创. First decide the primary purpose:

- 知识库积累：值得保存，方便以后查阅/建立认知素材，但暂时不需要二创。
- 二创素材：适合改写成你的账号定位（如知识科普、行业分析、个人成长/效率工具等）内容。
- 反面案例：适合拆灰色流量、PUA、焦虑营销或私域转化结构，不建议正向模仿。
- 仅归档/低价值：信息密度低或暂时无明显用途，只做记录。

When useful, map the item to the user's account matrix, but avoid overclaiming. Some notes should simply say "知识库积累：用于以后查阅某类观点/案例/话术结构，暂不建议二创".

If the user maintains a dedicated `个人形象管理/` knowledge area, file primarily-grooming/fitness/body-posture/skincare/energy-management style videos under `<your_vault_root>/个人形象管理/视频解析报告/` instead of the default self-media folder, keeping only an index row in `自媒体选题库/视频内容总表.md`. Use vault-root-relative wikilinks such as `[[个人形象管理/视频解析报告/douyin_xxx_解析报告]]`. Do not leave the detailed note in `自媒体选题库/视频解析报告/` if the primary topic belongs to a domain knowledge base.

The user may also maintain a `情感知识库/` area. If a parsed video is primarily about dating, intimacy, male/female relationship tactics, partner screening, sexual anxiety, PUA/manipulation, gender discourse, or relationship monetization, file the detailed note under `<your_vault_root>/情感知识库/视频解析报告/` and keep only an index row in `自媒体选题库/视频内容总表.md`. Use vault-root-relative wikilinks such as `[[情感知识库/视频解析报告/douyin_xxx_解析报告]]`. If the parser script first writes to the default self-media folder, rewrite/move the final structured note to the domain folder and remove the duplicate default note so Obsidian does not contain two competing copies.

For `风险/备注`, flag issues such as value-risk, unverifiable claims, parser/ASR failure, copyright/access limitations, or “只适合知识库积累/拆结构，不适合正向模仿”. For relationship/gray-traffic content, explicitly label value-risk such as class prejudice, gender stereotyping, manipulation, objectification, boundary issues, unverifiable folk psychology, or monetized anxiety; prefer `反面案例 + 知识库积累` unless the content is clearly healthy and reusable.

If parsing fails, still add a row only when the user seems to want tracking, with `内容类型=解析失败`, `核心观点=未获取到有效内容`, and a concise next-action note.

## Standard workflow

### 1. Accept input

Accept one public video URL. If the user provides more than one URL, process each independently and produce one report per URL or ask for batch behavior if the request is ambiguous.

### 2. Parse no-watermark media

Run the bundled script when code execution is available:

```bash
python scripts/parse_and_transcribe.py "https://example.com/video" --output report.md
```

The script will:

- call the configured parser endpoint;
- preserve the raw parser JSON for troubleshooting;
- recursively detect common metadata fields such as title, author, platform, publish time, description/content, video URL, audio URL, and cover URL;
- choose audio URL first if available, otherwise video URL;
- call DashScope ASR if `DASHSCOPE_API_KEY` is present;
- write a Markdown report.

If code execution is not available, explain the required command and ask the user to run it locally with the environment variables above.

### 3. Transcribe with Bailian / DashScope

Prefer DashScope long audio transcription via the Python SDK. Use `DASHSCOPE_ASR_MODEL` when set; otherwise use `paraformer-v2`.

If the ASR service rejects the media URL because it is not publicly reachable, expiring, or has unsupported format, report the parser metadata and failure clearly. Suggest downloading the media, uploading it to an accessible object storage location, and retrying with that URL.

### 3b. Xiaohongshu image-note OCR workflow

Xiaohongshu often returns `type=2`, `pics=[...]`, and no `video_url`. Do not treat this as a failed parse if image URLs are available. If the parser times out or returns a generic failure but the Xiaohongshu web page is accessible, fetch the HTML and extract `window.__INITIAL_STATE__` / `noteDetailMap` / `imageList` before giving up; see `references/xiaohongshu-html-state-fallback.md`. Instead:

1. Save the raw parser JSON as usual and read `data.desc`, `data.title`, `data.cover`, and `data.pics`.
2. Download all `pics` to a note-local asset directory using browser-like headers (`User-Agent: Mozilla/5.0`, `Referer: https://www.xiaohongshu.com/`).
3. Create a contact sheet from the downloaded images with page/file labels so the vision model can inspect the full carousel in one call.
4. Run image understanding/OCR on the contact sheet and extract the page-by-page structure, not just the caption.
5. Rewrite the Markdown report as a 图文笔记解析报告 with: basic info, one-sentence summary, page-by-page extraction, user value judgment, reusable topic angles, and actionable checklist.
6. Keep the summary row in `视频内容总表.md`; classify by primary content domain. For academic/productivity notes, `自媒体选题库/视频解析报告/` is acceptable unless a more specific knowledge-base folder exists.

See `references/xiaohongshu-image-notes.md` for command snippets and report-shaping details.

### 3c. Academic / paper-summary social notes

When a social post summarizes an academic paper or makes research claims, do not stop at the social caption. Treat the post as a lead: extract paper identifiers/title fragments, find the original arXiv/DOI/official source when available, read the source text, then produce a research-oriented note with paper explanation, subtask breakdown, research roadmap, user-specific implications, and source-verification caveats. See `references/academic-social-note-workflow.md`.

### 4. Generate final report

Always output Markdown using this structure:

```markdown
# 视频内容解析报告

## 基本信息

| 字段 | 内容 |
|---|---|
| 平台 |  |
| 标题 |  |
| 作者 |  |
| 发布时间 |  |
| 原始链接 |  |
| 无水印媒体链接 |  |

## 内容

[转写后的正文。若转写失败，则放已有标题、描述、caption 或解析接口返回的文本，并明确说明转写失败原因。]

## 关键词 / 标签

- 关键词1
- 关键词2
- 关键词3

## 备注

[可选：解析接口、ASR、媒体格式、置信度或失败信息。]
```

Keep the report factual. Do not invent missing author, publish time, or transcript text. Use `未知` for unavailable metadata.

### 4b. When the user asks for a picture / infographic

If the user asks to "提取内容核心并变成图片/发图片/做成图", still run the normal parse + transcript pipeline first, then create a concise structured report and a WeChat-friendly visual summary:

1. Extract the core into 3-5 sections, not a full transcript dump.
2. If the topic belongs to a domain vault (e.g. personal image/growth/energy management), save the detailed note there and put any generated image under that note folder's `assets/` directory.
3. Prefer a portrait 1080×1920 local PNG for WeChat delivery when hosted image generation is unnecessary or unavailable. Use PIL with a system Chinese font (e.g. on Windows `C:/Windows/Fonts/msyh.ttc` / `msyhbd.ttc`; on macOS `/System/Library/Fonts/PingFang.ttc`; on Linux a Noto CJK install), large readable cards, and CJK-aware wrapping.
4. Verify the image visually (vision tool or equivalent) before sending: check Chinese legibility, clipping, overlaps, footer visibility, and whether all key points are present.
5. Send the finished file with `MEDIA:/absolute/path/to/file` and also mention the Obsidian note/image paths.

For the infographic design workflow, consult `baoyu-infographic`; for simple summary cards, a deterministic local PIL script is usually faster and more reliable than prompting an image model.

### 5. Update the video content table

After the detailed report is written and verified, update `视频内容总表.md` in the Obsidian vault. If the file does not exist, create it with a short purpose statement, field definitions, and the default table header.

Recommended row-generation rules:

- `日期`: prefer video publish date; if unavailable, use parse date.
- `标题/主题`: concise human-readable title, not a raw filename.
- `内容类型`: classify the video, e.g. `AI 工具 / Agent 工作流`, `生活技能 / 标准答案型教程`, `男性情感 / 灰色流量案例`, `科研方法 / 论文阅读`.
- `核心观点`: one sentence that captures what the video argues or teaches.
- `可复用价值`: first label the purpose: `知识库积累` / `二创素材` / `反面案例` / `仅归档`. Then explain whether the user should save for later lookup, adapt into content, or only keep as a reference.
- `风险/备注`: include factual uncertainty, value-risk, parser failure, or platform limitations.
- `解析笔记`: use an Obsidian wikilink to the detailed note, e.g. `[[视频解析报告/douyin_123_结构化解析]]`.

Avoid duplicating rows: before appending, search the table for the video ID or original URL. If it exists, update that row rather than adding a second one.

## Keyword/tag extraction rules

When transcript text is available, extract 5-10 concise Chinese keywords or tags from the title and transcript. Prefer named entities, products, places, people, topics, and user-intent terms. Avoid generic tags such as “视频”, “内容”, “分享”, unless they are truly the topic.

If the transcript is short, use 3-5 tags. If ASR fails and only metadata is available, extract tags from title, description, and platform-provided labels only.

## Troubleshooting

- **Python 3.7 syntax check:** If the host Python is 3.7, avoid f-string expressions containing backslashes, e.g. `f"{v.replace('|', '\\|')}"` can raise `SyntaxError: f-string expression part cannot include a backslash`. Precompute the escaped value first:

  ```python
  safe_v = v.replace("|", r"\|")
  lines.append(f"| {k} | {safe_v} |")
  ```

- **Dependency setup:** Install DashScope when ASR is needed:

  ```bash
  python -m pip install --user dashscope
  ```

- Parser returns non-JSON: save the raw response and report that the parser response could not be interpreted.
- **Platform code normalization:** Some parser responses put opaque numeric codes such as `platform=1` or `type=1` in metadata. Do not surface these as the platform name in reports; infer the human platform from the original URL/domain (e.g. `douyin` → `抖音`) and patch old reports if needed.
- **Douyin parser fallback:** If a public Douyin link parser response is non-useful (e.g. `"Hello World"`, unknown title/media, or admin/contact text), do not stop there. Retry with `python -m yt_dlp --dump-json <url>` to get metadata and a playable media URL, then transcribe that URL with DashScope. If ASR still fails but yt-dlp can download the video, create a frame contact sheet and use vision/OCR to extract subtitles and on-screen workflow details before writing the report; mark it as OCR-based rather than a verbatim transcript. See `references/douyin-ytdlp-fallback.md`.
- **Bilibili fallback:** For Bilibili URLs, prefer `yt-dlp --dump-json` and Bilibili's public metadata/subtitle APIs over the no-watermark parser. If no subtitle exists, pick an audio-only format from yt-dlp JSON and send that URL to DashScope ASR. See `references/bilibili-ytdlp-asr.md`.
- No media URL found: show available metadata and state that no usable `video_url` or `audio_url` equivalent was found only after trying the platform-specific yt-dlp/API fallback when applicable.
- ASR authentication error: ask the user to verify `DASHSCOPE_API_KEY`.
- ASR async task times out: keep the parser result and tell the user to retry or use a shorter clip / externally hosted audio URL.
- Unsupported platform: report the parser error and avoid guessing.

## Bundled resources

- `scripts/parse_and_transcribe.py`: end-to-end parser + ASR + Markdown report generator. If DashScope returns only a `transcription_url`, the script must fetch that result JSON and extract transcript text from it instead of treating the ASR task as textless. For DashScope result JSON, prefer top-level `transcripts[*].text` over nested word/sentence fragments to avoid duplicated character-level output.
- `references/academic-social-note-workflow.md`: verify and analyze social posts that summarize academic papers; fetch original arXiv/DOI sources, extract PDF text, and produce user-focused task breakdowns/research roadmaps.
- `references/bilibili-ytdlp-asr.md`: Bilibili metadata/subtitle API plus yt-dlp audio-only URL to DashScope ASR fallback workflow.
- `references/configuration.md`: environment variables, local setup, and expected parser/API behavior.
- `references/douyin-ytdlp-fallback.md`: fallback workflow for Douyin links when the parser returns empty/invalid content.
- `references/douyin-ytdlp-ocr-fallback.md`: second-stage Douyin fallback when ASR fails but yt-dlp can download video; build frame contact sheets and use vision/OCR to write a non-verbatim structured report.
- `references/hermes-local-env.md`: Hermes-specific `.env.local` setup, script bootstrap pattern, and verification probe.
- `references/relationship-gray-traffic.md`: relationship/dating/PUA/gray-traffic video routing, value-risk labels, and ethical migration patterns for the user's knowledge base.
- `references/xiaohongshu-image-notes.md`: Xiaohongshu carousel/image-note workflow: download `pics`, build a contact sheet, OCR with vision, and rewrite a value-oriented report.
- `references/xiaohongshu-html-state-fallback.md`: fallback for public Xiaohongshu notes when the parser times out but the page HTML contains `__INITIAL_STATE__`, `noteDetailMap`, `desc`, author, and image URLs.
- `references/video-knowledge-table.md`: Obsidian video content table schema, row template, classification hints, and update workflow.
