#!/usr/bin/env python3
"""Parse a social-video URL, transcribe it with Alibaba Bailian/DashScope, and write Markdown.

This script is intentionally schema-tolerant: parser APIs often return different
field names by platform. It recursively searches for common media and metadata
keys, keeps the raw response, and avoids inventing missing data.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Any, Iterable

import requests

DEFAULT_PARSER_BASE_URL = os.environ.get("SOCIAL_VIDEO_PARSER_BASE_URL", "")
DEFAULT_MODEL = "paraformer-v2"


def load_env_file(path: Path) -> None:
    """Load simple KEY=VALUE lines without overwriting existing environment variables."""
    if not path.exists() or not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def bootstrap_env() -> None:
    """Load skill-local config so Hermes/Gateway runs do not require shell exports."""
    skill_root = Path(__file__).resolve().parents[1]
    for env_path in [skill_root / ".env", skill_root / ".env.local"]:
        load_env_file(env_path)


bootstrap_env()

PLATFORM_HINTS = {
    "douyin": "抖音",
    "iesdouyin": "抖音",
    "bilibili": "Bilibili",
    "b23.tv": "Bilibili",
    "youtube": "YouTube",
    "youtu.be": "YouTube",
    "xiaohongshu": "小红书",
    "xhslink": "小红书",
    "tiktok": "TikTok",
    "kuaishou": "快手",
    "weibo": "微博",
}

FIELD_CANDIDATES = {
    "platform": ["platform", "source", "site", "app", "type"],
    "title": ["title", "desc", "description", "caption", "content", "text"],
    "author": ["author", "nickname", "nick_name", "username", "user_name", "name"],
    "publish_time": ["publish_time", "published_at", "create_time", "created_at", "time", "date", "timestamp"],
    "content": ["content", "desc", "description", "caption", "text"],
    "video_url": [
        "video_url",
        "video",
        "play_url",
        "playurl",
        "download_url",
        "downloadurl",
        "wm_free_url",
        "nowatermark_url",
        "no_watermark_url",
        "media_url",
        "url",
    ],
    "audio_url": ["audio_url", "audio", "music_url", "music", "sound_url", "mp3", "m4a"],
    "cover_url": ["cover", "cover_url", "poster", "thumbnail", "thumb", "image"],
}

URL_RE = re.compile(r"^https?://", re.I)


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def is_url(value: Any) -> bool:
    return isinstance(value, str) and bool(URL_RE.match(value.strip()))


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return str(value)
    if not isinstance(value, str):
        return ""
    return re.sub(r"\s+", " ", value).strip()


def iter_nodes(obj: Any) -> Iterable[tuple[str, Any]]:
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield str(key), value
            yield from iter_nodes(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from iter_nodes(item)


def first_by_keys(obj: Any, keys: list[str], require_url: bool = False) -> str:
    wanted = {k.lower() for k in keys}
    for key, value in iter_nodes(obj):
        lk = key.lower()
        if lk not in wanted:
            continue
        if isinstance(value, list):
            for item in value:
                if require_url and is_url(item):
                    return item.strip()
                text = clean_text(item)
                if text and not require_url:
                    return text
        elif isinstance(value, dict):
            for nested_key in ["url", "src", "href", "play_url", "download_url"]:
                nested = value.get(nested_key)
                if require_url and is_url(nested):
                    return nested.strip()
        else:
            if require_url and is_url(value):
                return value.strip()
            text = clean_text(value)
            if text and not require_url:
                return text
    return ""


def normalize_time(value: str) -> str:
    value = clean_text(value)
    if not value:
        return ""
    if value.isdigit():
        n = int(value)
        # 13-digit millisecond timestamps are common.
        if n > 10_000_000_000:
            n //= 1000
        if 946684800 <= n <= 4102444800:
            return dt.datetime.fromtimestamp(n).strftime("%Y-%m-%d %H:%M:%S")
    return value


def infer_platform(url: str, parsed: dict[str, str]) -> str:
    platform = (parsed.get("platform") or "").strip()
    lower_url = url.lower()
    # Some parser endpoints return numeric app/type codes such as "1" for Douyin;
    # prefer the original URL/domain hint over opaque numeric labels.
    if platform and not platform.isdigit():
        return PLATFORM_HINTS.get(platform.lower(), platform)
    for needle, name in PLATFORM_HINTS.items():
        if needle in lower_url:
            return name
    return platform or "未知"


def fetch_parser(url: str, parser_base_url: str, timeout: int) -> tuple[Any, str]:
    endpoint = parser_base_url + urllib.parse.quote_plus(url)
    response = requests.get(endpoint, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    text = response.text
    try:
        return response.json(), text
    except json.JSONDecodeError:
        return {"raw_text": text}, text


def parse_metadata(url: str, data: Any) -> dict[str, str]:
    result: dict[str, str] = {}
    for field, keys in FIELD_CANDIDATES.items():
        result[field] = first_by_keys(data, keys, require_url=field.endswith("_url"))
    result["platform"] = infer_platform(url, result)
    result["publish_time"] = normalize_time(result.get("publish_time", ""))
    result["media_url"] = result.get("audio_url") or result.get("video_url")
    return result


def transcribe_with_dashscope_sdk(media_url: str, model: str, api_key: str, timeout: int) -> tuple[str, Any]:
    import dashscope  # type: ignore
    from dashscope.audio.asr import Transcription  # type: ignore

    dashscope.api_key = api_key
    task_response = Transcription.async_call(model=model, file_urls=[media_url])
    task_id = getattr(getattr(task_response, "output", None), "task_id", None)
    if not task_id and isinstance(task_response, dict):
        task_id = task_response.get("output", {}).get("task_id")
    if not task_id:
        raise RuntimeError(f"DashScope did not return a task_id: {task_response}")

    deadline = time.time() + timeout
    last_response: Any = None
    while time.time() < deadline:
        last_response = Transcription.wait(task=task_id)
        status_code = getattr(last_response, "status_code", None)
        output = getattr(last_response, "output", None)
        if isinstance(last_response, dict):
            status_code = last_response.get("status_code", status_code)
            output = last_response.get("output", output)
        if status_code == 200 and output:
            text = extract_transcript_text(output)
            if not text:
                transcription_url = first_by_keys(output, ["transcription_url"], require_url=True)
                if transcription_url:
                    transcript_json = requests.get(transcription_url, timeout=60).json()
                    text = extract_transcript_text(transcript_json)
            if text:
                return text, last_response
        status = ""
        if isinstance(output, dict):
            status = str(output.get("task_status", ""))
        else:
            status = str(getattr(output, "task_status", ""))
        if status.upper() in {"FAILED", "CANCELED", "UNKNOWN"}:
            raise RuntimeError(f"DashScope ASR task failed: {last_response}")
        time.sleep(5)
    raise TimeoutError(f"DashScope ASR task timed out after {timeout} seconds: {last_response}")


def extract_transcript_text(obj: Any) -> str:
    # DashScope result JSON commonly has top-level transcripts[*].text plus many
    # word/sentence fragments. Prefer the full transcript field to avoid noisy
    # duplicated character-level output.
    if isinstance(obj, dict) and isinstance(obj.get("transcripts"), list):
        full_texts: list[str] = []
        for item in obj["transcripts"]:
            if isinstance(item, dict):
                text = clean_text(item.get("text"))
                if text and not is_url(text) and text not in full_texts:
                    full_texts.append(text)
        if full_texts:
            return "\n".join(full_texts).strip()

    pieces: list[str] = []
    for key, value in iter_nodes(obj):
        lk = key.lower()
        if lk in {"text", "transcript", "sentence", "content"}:
            text = clean_text(value)
            if text and not is_url(text) and text not in pieces:
                pieces.append(text)
    return "\n".join(pieces).strip()


def transcribe(media_url: str, model: str, timeout: int) -> tuple[str, str, Any]:
    api_key = os.getenv("DASHSCOPE_API_KEY", "").strip()
    if not api_key:
        return "", "未设置 DASHSCOPE_API_KEY，已跳过语音转文字。", None
    try:
        text, raw = transcribe_with_dashscope_sdk(media_url, model, api_key, timeout)
        return text, "", raw
    except ImportError:
        return "", "未安装 dashscope Python SDK。请运行 `python -m pip install dashscope` 后重试。", None
    except Exception as exc:  # Keep failure visible in the report.
        return "", f"语音转文字失败：{exc}", None


def simple_keywords(text: str, limit: int = 8) -> list[str]:
    # Lightweight fallback only. ChatGPT should refine final tags when using the skill.
    cleaned = re.sub(r"https?://\S+", " ", text)
    tokens = re.findall(r"[\u4e00-\u9fff]{2,8}|[A-Za-z][A-Za-z0-9_+-]{2,}", cleaned)
    stop = {"这个", "一个", "我们", "你们", "他们", "大家", "视频", "内容", "就是", "可以", "没有", "进行", "因为", "所以"}
    counts: dict[str, int] = {}
    for token in tokens:
        if token in stop:
            continue
        counts[token] = counts.get(token, 0) + 1
    return [word for word, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]]


def markdown_report(original_url: str, metadata: dict[str, str], transcript: str, asr_note: str) -> str:
    title = metadata.get("title") or "未知标题"
    content = transcript or metadata.get("content") or metadata.get("title") or "未获取到可用文本内容。"
    keywords = simple_keywords(f"{title}\n{content}")
    media_url = metadata.get("media_url") or "未知"
    rows = [
        ("平台", metadata.get("platform") or "未知"),
        ("标题", title),
        ("作者", metadata.get("author") or "未知"),
        ("发布时间", metadata.get("publish_time") or "未知"),
        ("原始链接", original_url),
        ("无水印媒体链接", media_url),
    ]
    lines = [
        "# 视频内容解析报告",
        "",
        "## 基本信息",
        "",
        "| 字段 | 内容 |",
        "|---|---|",
    ]
    for k, v in rows:
        safe_v = v.replace("|", r"\|")
        lines.append(f"| {k} | {safe_v} |")
    lines += ["", "## 内容", "", content.strip(), "", "## 关键词 / 标签", ""]
    if keywords:
        lines += [f"- {kw}" for kw in keywords]
    else:
        lines.append("- 未提取到关键词")
    if asr_note:
        lines += ["", "## 备注", "", asr_note]
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse and transcribe a social video URL.")
    parser.add_argument("url", help="Public social-video URL to parse")
    parser.add_argument("--output", "-o", help="Markdown output path")
    parser.add_argument("--raw-json", help="Path to save raw parser JSON")
    parser.add_argument("--no-transcribe", action="store_true", help="Skip ASR and only parse metadata/media URL")
    parser.add_argument("--parser-base-url", default=os.getenv("SOCIAL_VIDEO_PARSER_BASE_URL", DEFAULT_PARSER_BASE_URL))
    parser.add_argument("--model", default=os.getenv("DASHSCOPE_ASR_MODEL", DEFAULT_MODEL))
    parser.add_argument("--timeout", type=int, default=600, help="ASR timeout in seconds")
    args = parser.parse_args()

    output_dir = Path(os.getenv("SOCIAL_VIDEO_OUTPUT_DIR", ".")).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = "social_video_report_" + dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(args.output) if args.output else output_dir / f"{stem}.md"
    raw_path = Path(args.raw_json) if args.raw_json else output_dir / f"{stem}.parser.json"

    data, raw_text = fetch_parser(args.url, args.parser_base_url, timeout=30)
    raw_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    metadata = parse_metadata(args.url, data)

    transcript = ""
    asr_note = ""
    if metadata.get("media_url") and not args.no_transcribe:
        transcript, asr_note, _ = transcribe(metadata["media_url"], args.model, args.timeout)
    elif not metadata.get("media_url"):
        asr_note = "解析接口未返回可用的音频或视频链接，已跳过语音转文字。"
    else:
        asr_note = "用户选择跳过语音转文字。"

    report = markdown_report(args.url, metadata, transcript, asr_note)
    output_path.write_text(report, encoding="utf-8")
    print(str(output_path))
    eprint(f"raw parser json: {raw_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
