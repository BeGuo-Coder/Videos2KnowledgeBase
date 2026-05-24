# Bilibili yt-dlp + DashScope ASR fallback

Use this when the user provides a Bilibili URL and asks for parsing/transcription/summary/table update.

## Why

Bilibili often has reliable metadata through `yt-dlp` and public APIs, but may not provide uploader subtitles. The robust fallback is:

1. Extract metadata/formats with `yt-dlp --dump-json`.
2. Query Bilibili public API for title/owner/cid if needed.
3. Check subtitle API.
4. If subtitles are absent, send an audio-only format URL to DashScope ASR.
5. Write the detailed report and update the `视频内容总表.md` in your vault.

## Commands

Use the system Python (or whichever Python has an up-to-date `yt-dlp` installed). Adjust the interpreter path below to your own environment:

```bash
python -m yt_dlp --dump-json 'https://www.bilibili.com/video/BVxxxx' > '<your_vault_root>/自媒体选题库/视频解析报告/bilibili_BVxxxx.ytdlp.json'
```

If `yt-dlp` is missing for that interpreter:

```bash
python -m pip install --user -q yt-dlp
```

## Metadata API

```python
import requests
bvid = 'BVxxxx'
r = requests.get(
    'https://api.bilibili.com/x/web-interface/view',
    params={'bvid': bvid},
    headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.bilibili.com/'},
    timeout=30,
)
data = r.json()['data']
aid, cid, title, owner = data['aid'], data['cid'], data['title'], data['owner']['name']
```

## Subtitle API

```python
r = requests.get(
    'https://api.bilibili.com/x/player/v2',
    params={'bvid': bvid, 'cid': cid},
    headers={'User-Agent': 'Mozilla/5.0', 'Referer': f'https://www.bilibili.com/video/{bvid}'},
    timeout=30,
)
subtitles = r.json().get('data', {}).get('subtitle', {}).get('subtitles', [])
```

If `subtitles` is non-empty, fetch the subtitle URL and summarize it. If empty, use ASR.

## Selecting audio for ASR

From the yt-dlp JSON, choose the first audio-only format:

```python
audio = next(
    f['url'] for f in info['formats']
    if f.get('vcodec') == 'none' and f.get('acodec') not in {None, 'none'}
)
```

Then call DashScope long ASR using the skill-local `.env.local` for `DASHSCOPE_API_KEY`. Store raw transcript JSON and cleaned text next to the report:

```text
bilibili_<BV>.transcript.json
bilibili_<BV>.transcript.txt
```

## Report and table update

Name detailed notes like:

```text
bilibili_<BV>_结构化解析.md
```

Add/update one row in:

```text
<your_vault_root>/自媒体选题库/视频内容总表.md
```

Use an Obsidian wikilink:

```markdown
[[视频解析报告/bilibili_<BV>_结构化解析]]
```

## Pitfalls

- Bilibili `yt-dlp` output may not include `aid/cid`; use the public `x/web-interface/view` API.
- `subtitles` may be empty even when the video has speech; use audio-only ASR fallback.
- Keep metadata factual. Do not infer missing subtitles, author details, or upload stats beyond API/yt-dlp output.
- Some Bilibili audio URLs are expiring CDN URLs; run ASR soon after extracting them.
- DashScope may fail on Bilibili CDN URLs with `FILE_403_FORBIDDEN` because the service cannot supply required headers. In that case, download audio locally with `yt-dlp -f 30216 -o <asset_dir>/audio.%(ext)s <url>` and run local ASR if available. On a Windows host with Anaconda, `python -m pip install --user -q faster-whisper` works with Python 3.9; transcribe via `WhisperModel('small', device='cpu', compute_type='int8').transcribe(audio_path, language='zh', vad_filter=True, beam_size=5)`, then save `<BV>.transcript.txt` and `<BV>.transcript_segments.json` next to the report. Note in the report that local ASR may have homophone/traditional-character errors and should be semantically cleaned.
