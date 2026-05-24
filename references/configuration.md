# Configuration Reference

## Environment variables

| Variable | Required | Default | Purpose |
|---|---:|---|---|
| `DASHSCOPE_API_KEY` | yes for ASR | none | Alibaba Cloud Model Studio / Bailian DashScope API key. |
| `DASHSCOPE_ASR_MODEL` | no | `paraformer-v2` | ASR model name. |
| `SOCIAL_VIDEO_PARSER_BASE_URL` | no | bundled parser URL | Parser prefix. The original video URL is URL-encoded and appended to this value. |
| `SOCIAL_VIDEO_OUTPUT_DIR` | no | current directory | Directory for reports and raw parser JSON. |

## Parser expectations

The parser endpoint is expected to accept a GET request where the original URL is appended as the `url` query parameter value. The response should preferably be JSON. The script recursively searches for common fields including:

- platform: `platform`, `source`, `app`, `site`
- title: `title`, `desc`, `description`, `caption`
- author: `author`, `nickname`, `username`, `user.name`
- publish time: `publish_time`, `create_time`, `created_at`, `time`, `date`
- media URL: `video_url`, `play_url`, `download_url`, `url`, `audio_url`, `music_url`

If the parser returns a different schema, update `scripts/parse_and_transcribe.py` field candidates rather than changing the report format.

## Bailian / DashScope ASR behavior

The script uses the DashScope Python SDK when available and falls back to the DashScope HTTP task API when possible. Long-audio ASR services usually require a network-accessible file URL. If the parser's media URL expires quickly or requires cookies, transcribe immediately or upload the media to accessible object storage first.

## Local setup

```bash
python -m pip install requests dashscope
export DASHSCOPE_API_KEY="your_api_key"
python scripts/parse_and_transcribe.py "https://example.com/video" --output report.md
```
