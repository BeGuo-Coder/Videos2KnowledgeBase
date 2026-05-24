# Academic social-note workflow

Use when a social-media post (especially Xiaohongshu) summarizes, claims, or discusses an academic paper and the user asks to understand the paper, split tasks, or produce a research roadmap.

## Goal

Do not stop at the social caption. Treat the post as a lead, verify the original academic source, and turn it into a value-oriented research note for the user.

## Workflow

1. Parse the social link normally and preserve the parser JSON/report.
2. Extract academic identifiers and search cues from title/caption/images:
   - paper title fragments;
   - arXiv ID / DOI / conference name;
   - distinctive numbers, benchmark names, system names, author names.
3. Search for the original source when the post is a secondary summary. Prefer arXiv/DOI/official conference pages over reposted news.
4. If an arXiv/PDF source is found, fetch and extract text before analysis:
   ```bash
   python - <<'PY'
   import requests, pathlib
   url='https://export.arxiv.org/pdf/<id>'
   p=pathlib.Path('<tmp_dir>/<paper>.pdf')
   r=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=60)
   r.raise_for_status(); p.write_bytes(r.content)
   print(p)
   PY
   pdftotext '<tmp_dir>/<paper>.pdf' '<tmp_dir>/<paper>.txt'
   ```
   Replace `<tmp_dir>` with a writable temp path on your system (e.g. `/tmp/` on macOS/Linux, or an existing drive path like `D:/tmp/` on Windows/Git Bash where `/tmp` may not resolve).
   If `requests` fails with a partial/chunked PDF download, retry with curl instead of treating the source as unavailable:
   ```bash
   curl -L --retry 3 -A 'Mozilla/5.0' -o '<tmp_dir>/<paper>.pdf' 'https://arxiv.org/pdf/<id>'
   pdftotext '<tmp_dir>/<paper>.pdf' '<tmp_dir>/<paper>.txt'
   ```
5. Read the abstract, introduction, method/system section, results/survey/evaluation section, and conclusion. Pull key numbers from the source text, not just the social post. For method papers, also capture project/code links, benchmark construction, main result table values, ablations, and stated limitations.
6. Write a cleaned Markdown note under the user's relevant vault area. For research/social notes, use `自媒体选题库/视频解析报告/` unless a domain-specific area exists.
7. Include sections beyond a normal transcript report:
   - basic info and source verification;
   - one-sentence summary;
   - social-post claim extraction;
   - paper explanation in plain Chinese;
   - key results and limitations;
   - subtask breakdown;
   - research routes / reproduction roadmap;
   - direct implications for the user's papers/accounts;
   - risks/what must be cited from the original paper.
8. Update `视频内容总表.md` with `内容类型=科研方法 / 论文阅读 / <specific topic>`, and flag secondary-source uncertainty in `风险/备注`.

## Report-shaping notes

- Prioritize practical research routing over generic summary. Always add "下一步行动建议" when the post is research-relevant.
- For paper/tool posts, map the idea to the user's current research when plausible, but label speculative extensions as such.
- If the social post is a secondary summary, explicitly state "严谨引用以原论文为准".
- For AI-reviewer / paper-review posts, useful reusable outputs include: task decomposition, benchmark ideas, self-review checklist, and how to apply it to the user's current research direction.

## Pitfalls

- Do not treat caption-only parser output as complete if the post discusses a paper with a retrievable source.
- Do not cite social-media numbers as authoritative until checked against the original paper.
- Do not overbuild a full systematic literature review unless the user asks; this workflow is a targeted source-verification + research-roadmap note.
