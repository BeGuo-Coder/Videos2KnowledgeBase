# Douyin yt-dlp + frame OCR fallback

Use when the default parser returns generic failure text or an unusable `m.douyin.com/share/video/...` URL, and DashScope ASR cannot decode the media URL.

## Workflow

1. Get authoritative metadata and playable formats:

```bash
python -m yt_dlp --dump-json '<douyin-share-url>' > /tmp/douyin.json
```

Extract: `id`, `title`, `description`, `creator`, `upload_date`, `duration`, and a playable `url` / `format_id`.

2. Download a local copy for analysis:

```bash
mkdir -p '<note-dir>/assets'
python -m yt_dlp -f 'best' -o '<note-dir>/assets/douyin_%(id)s.%(ext)s' '<douyin-share-url>'
```

3. Build a contact sheet for vision/OCR when ASR fails:

```bash
mkdir -p '<note-dir>/assets/douyin_<id>_frames'
ffmpeg -y -i '<note-dir>/assets/douyin_<id>.mp4' \
  -vf 'fps=1/3,scale=360:-1' \
  '<note-dir>/assets/douyin_<id>_frames/frame_%03d.jpg'
```

Then use PIL to tile frames in reading order, adding labels like `01 t≈0s`, `02 t≈3s`, etc. Use vision on the contact sheet to extract subtitles, tools, screen text, and workflow steps.

4. Write the report clearly as OCR-based:

```markdown
> 说明：原解析接口/ASR 未成功，以下内容基于 yt-dlp 元数据 + 视频截图 OCR/字幕抽取整理，可能不是逐字稿。
```

5. If an earlier failed report was written to the default output path, replace it with the final structured note and delete the failed duplicate so the Obsidian vault has one canonical note.

## Report shaping

For tool/workflow videos, prioritize:
- tool/project names and repository paths;
- on-screen evidence (dashboards, numbers, UI labels) with uncertainty words like "约/画面显示"；
- workflow sequence (`业务流程 → 规则/SOP → skill/prompt → AI执行 → 人工审核`);
- reuse mapping to the user's account matrix (e.g. AI 本地商家、账号矩阵、科研/论文流程自动化);
- risks: claimed revenue/customer counts require verification; automated posting must respect platform rules.
