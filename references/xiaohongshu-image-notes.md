# Xiaohongshu image-note parsing workflow

Use when a Xiaohongshu URL is a carousel/image note rather than a video. Parser signs include `data.type = 2`, `data.pics` contains image URLs, and `video_url` is empty.

## Workflow

1. Run the normal parser script first:

```bash
python scripts/parse_and_transcribe.py '<xiaohongshu-url>' --output '<vault>/自媒体选题库/视频解析报告/xiaohongshu_<id>_解析报告.md'
```

2. Read the saved `.parser.json`. Extract:

- `data.desc` / `data.title` for caption and title
- `data.userId` if author is unavailable
- `data.cover`
- `data.pics[]` image URLs

3. Download images into an asset folder next to the report. Xiaohongshu CDN may require browser-like headers:

```python
import os, urllib.request
pics = [...]
outdir = '.../xhs_<id>_images'
os.makedirs(outdir, exist_ok=True)
for i, url in enumerate(pics, 1):
    path = f'{outdir}/image_{i:02d}.jpg'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://www.xiaohongshu.com/',
    })
    with urllib.request.urlopen(req, timeout=30) as r, open(path, 'wb') as f:
        f.write(r.read())
```

4. Build a contact sheet so one vision call can inspect the whole carousel:

```python
from PIL import Image, ImageDraw
import glob, os, math
paths = sorted(glob.glob(f'{outdir}/image_*.jpg'))
thumbs = []
for p in paths:
    im = Image.open(p).convert('RGB')
    im.thumbnail((360, 640))
    canvas = Image.new('RGB', (380, 700), 'white')
    d = ImageDraw.Draw(canvas)
    d.text((10, 10), os.path.basename(p), fill='black')
    canvas.paste(im, ((380 - im.width)//2, 40))
    thumbs.append(canvas)
cols = 2
rows = math.ceil(len(thumbs) / cols)
sheet = Image.new('RGB', (cols * 380, rows * 700), 'white')
for idx, im in enumerate(thumbs):
    sheet.paste(im, ((idx % cols) * 380, (idx // cols) * 700))
sheet.save(f'{outdir}/contact_sheet.jpg', quality=92)
```

5. Ask vision to read the contact sheet page-by-page. Prompt shape:

```text
请逐张阅读这组小红书笔记图片中的文字，尽量完整提取每页标题、要点和结构，并总结整篇笔记讲什么。
```

6. Rewrite the report. Include:

- `# 小红书笔记解析报告：<title>`
- Basic info table with platform, title, author if visible, publish time if visible, original URL, note type, local image asset link
- One-sentence summary
- Page-by-page extraction / original structure
- Keywords/tags
- Value judgment: content type, value level, account-matrix reuse, risks/remarks
- Reusable topic angles
- Concrete checklist if the note is actionable

7. Update `自媒体选题库/视频内容总表.md` with one row. Use the canonical item URL without long tracking query when possible, and link to the rewritten Markdown note.

## Direct web fallback when parser times out

If the no-watermark/parser endpoint returns a timeout or generic failure for a public Xiaohongshu note, do not stop immediately. Try direct page fetch with browser-like headers; Xiaohongshu often embeds enough note data in the HTML for public web shares.

```python
import json, re, requests
from bs4 import BeautifulSoup

url = '<xiaohongshu-url>'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36',
    'Referer': 'https://www.xiaohongshu.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
html = requests.get(url, headers=headers, timeout=30).text

def grab(key):
    m = re.search(r'"' + re.escape(key) + r'":"((?:\\\\.|[^"\\\\])*)"', html)
    return json.loads('"' + m.group(1) + '"') if m else ''

# Useful keys observed in noteDetailMap HTML state:
# noteId, desc, title, user.nickname, imageList[].urlDefault/infoList[].url
note_id = grab('noteId')
desc = grab('desc')
nickname = grab('nickname')
image_urls = []
for m in re.finditer(r'"url(?:Default|Pre)?":"((?:\\\\.|[^"\\\\])*)"', html):
    u = json.loads('"' + m.group(1) + '"')
    if 'xhscdn.com' in u and ('sns-webpic' in u or 'spectrum' in u) and u not in image_urls:
        image_urls.append(u)
```

Then continue with the normal image-download + contact-sheet + OCR workflow. Treat duplicated `urlPre` / `urlDefault` variants as the same page when they have the same visual content.

## Pitfalls

- Do not stop at caption-only output when `pics[]` exists. The core content of Xiaohongshu image notes is often in the images.
- Do not treat parser timeout as final when the public web page returns HTML; try the direct HTML `noteDetailMap` fallback above before marking it failed.
- Do not force the report into a video/transcript structure. Label it as 图文笔记解析报告 when appropriate.
- Keep raw parser JSON and extracted HTML-state JSON for traceability, but the user-facing note should be cleaned and value-oriented.
- If the images are primarily about personal image/grooming/fitness/mental state, file the detailed note under `个人形象管理/视频解析报告/` per the main skill instructions.
