# Douyin yt-dlp fallback

Use this when the configured no-watermark parser returns non-useful output such as `"Hello World"`, no media URL, or only an admin/contact message for a public Douyin short link.

## Pattern

1. Prefer the original Douyin short share link when available:

```bash
python -m yt_dlp --dump-json 'https://v.douyin.com/<code>/' > '<output_dir>/douyin_<id>.ytdlp.json'
```

If the user provided a `jingxuan?modal_id=<id>` link and the parser returns empty/unknown output, derive the canonical candidate and try it as a fallback:

```bash
python -m yt_dlp --dump-json 'https://www.douyin.com/video/<id>' > '<output_dir>/douyin_<id>.ytdlp.json'
```

If `yt-dlp` is not installed in the active Python:

```bash
python -m pip install --user yt-dlp
```

2. If yt-dlp says fresh cookies are needed, try a newer Python/yt-dlp install if available, but do not spend the session looping on browser-cookie extraction. Ask the user for one of: the full copied share text/short link, exported Netscape cookies, a downloaded video file, or screenshots/title for a partial content analysis.

3. Read the JSON fields:

- `id` / `display_id`: Douyin item id
- `title` or `description`: caption
- `creator`: author
- `timestamp`: publish time
- `duration_string`: duration
- `url`: selected playable MP4 URL
- `formats[*].url`: fallback media URLs

3. Transcribe the selected `url` with DashScope ASR. DashScope often returns a `transcription_url`; fetch that JSON and prefer `transcripts[*].text` for the clean full transcript.

4. Generate the report from yt-dlp metadata + ASR transcript. Mark media as watermarked/direct playback if yt-dlp format says so; do not claim no-watermark unless the parser provides one.

## Minimal metadata probe

```bash
python - <<'PY'
import json, datetime, pathlib
info=json.loads(pathlib.Path('douyin_item.ytdlp.json').read_text(encoding='utf-8'))
print(info.get('id'))
print(info.get('title') or info.get('description'))
print(info.get('creator'))
print(info.get('duration_string'))
if info.get('timestamp'):
    print(datetime.datetime.fromtimestamp(info['timestamp']).strftime('%Y-%m-%d %H:%M:%S'))
print(info.get('url'))
PY
```

## Pitfalls

- Do not stop after the parser creates an empty/unknown Markdown report; retry via yt-dlp before reporting failure.
- For `jingxuan?modal_id=<id>` links, try both the original URL and `https://www.douyin.com/video/<id>`; the former may be unsupported by yt-dlp while the latter may require cookies.
- If yt-dlp requires fresh cookies and browser-cookie extraction fails, treat that as an access/context limitation for this item. Ask for the complete copied share text/short link, exported cookies, or the video file instead of repeating the same extraction command.
- Douyin short links may redirect to `https://www.douyin.com/video/<id>...`; yt-dlp can usually extract from the original short link directly.
- yt-dlp may identify the extractor as `TikTok` while still returning Douyin metadata and URLs; this is acceptable.
- The selected `url` can expire. Run ASR soon after extraction or re-run yt-dlp to refresh it.
