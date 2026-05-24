# Xiaohongshu HTML `__INITIAL_STATE__` fallback

Use this when the normal parser endpoint times out or returns a generic failure for a public Xiaohongshu note, but the web page itself is accessible.

## Trigger signs

- Parser JSON has `code: 504`, `msg: 解析超时`, or `desc: 解析失败`.
- The generated report is captionless / says parse failed.
- A direct `requests.get()` of the Xiaohongshu URL returns HTML containing `window.__INITIAL_STATE__`, `noteDetailMap`, `desc`, `imageList`, or OpenGraph metadata.

## Fallback workflow

1. Fetch the page with browser-like headers:

```python
import requests
url = '<xiaohongshu share URL>'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36',
    'Referer': 'https://www.xiaohongshu.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
html = requests.get(url, headers=headers, timeout=30).text
```

2. Look for embedded state or metadata:

```python
for key in ['window.__INITIAL_STATE__', 'noteDetailMap', 'imageList', 'og:title']:
    print(key, html.find(key))
```

3. Extract values from the embedded JSON-ish HTML. Regex is often sufficient for concise fallback extraction:

```python
import re, json

def grab(key):
    m = re.search(r'"' + re.escape(key) + r'":"((?:\\.|[^"\\])*)"', html)
    return json.loads('"' + m.group(1) + '"') if m else ''

meta = {
    'desc': grab('desc'),
    'title': grab('title'),
    'nickname': grab('nickname'),
}

urls = []
for m in re.finditer(r'"url(?:Default|Pre)?":"((?:\\.|[^"\\])*)"', html):
    u = json.loads('"' + m.group(1) + '"')
    if 'xhscdn.com' in u and ('sns-webpic' in u or 'spectrum' in u) and u not in urls:
        urls.append(u)
meta['image_urls'] = urls
```

4. Prefer a human title from OpenGraph (`og:title`) or user-provided share text when generic values like `小红书_沪ICP备` appear in `title`.

5. Download `image_urls` with browser-like headers and continue the standard Xiaohongshu image-note workflow: build a contact sheet, run vision/OCR, write a cleaned report, and update the index table.

## Pitfalls

- Do not leave the parser-generated failure report as the final note if embedded HTML state contains usable `desc`, author, and images.
- Xiaohongshu may include multiple duplicate/preview URLs. Deduplicate and prefer `urlDefault` / higher-quality `WB_DFT` style URLs when available.
- The HTML title field can be generic site text; use `og:title`, share text, or extracted note detail title instead.
- Treat this as a fallback for public content only; do not bypass login-only/private content or access controls.
