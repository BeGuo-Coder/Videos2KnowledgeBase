# Hermes local environment setup for social-video-transcriber

Use this when the skill is installed manually into Hermes and should work from gateway platforms such as WeChat.

## Recommended `.env.local`

Create the file next to `SKILL.md`:

```text
<your_hermes_root>/.hermes/skills/media/social-video-transcriber/.env.local
```

Example:

```bash
DASHSCOPE_API_KEY="your_api_key"
DASHSCOPE_ASR_MODEL="paraformer-v2"
SOCIAL_VIDEO_OUTPUT_DIR="<your_vault_root>/自媒体选题库/视频解析报告"
```

Do not print the API key in final responses. Confirm only that it is configured.

## Script bootstrap pattern

If the script only reads process environment variables, add this pattern near the top after constants and before defaults are consumed:

```python
def load_env_file(path: Path) -> None:
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
    skill_root = Path(__file__).resolve().parents[1]
    for env_path in [skill_root / ".env", skill_root / ".env.local"]:
        load_env_file(env_path)

bootstrap_env()
```

## Verification probe

```bash
python - <<'PY'
import os, runpy, pathlib, importlib.util, py_compile
p=pathlib.Path('<your_hermes_root>/.hermes/skills/media/social-video-transcriber/scripts/parse_and_transcribe.py')
py_compile.compile(str(p), doraise=True)
runpy.run_path(str(p), run_name='skill_probe')
print('syntax=ok')
print('dashscope=', 'OK' if importlib.util.find_spec('dashscope') else 'MISSING')
print('api_key_loaded=', bool(os.environ.get('DASHSCOPE_API_KEY')))
print('output_dir=', os.environ.get('SOCIAL_VIDEO_OUTPUT_DIR'))
PY
```

Expected: syntax OK, dashscope OK when installed, key loaded true, and the configured output directory printed.
