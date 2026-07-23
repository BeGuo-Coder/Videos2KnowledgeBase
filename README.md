# FlowGate Video Parser Skill

> **5 分钟搭好一个内容采集 Skill。**  
> 从此，刷短视频不只是消费内容，而是在给你的知识银行持续“存钱”。

FlowGate Video Parser 是一个面向 Claude Code / AI Agent 的轻量级 Skill。

你只需要复制一条公开的短视频或图文链接，它就能自动完成媒体解析、语音转写、图片文字识别、文本纠错和 Markdown 整理，把信息流中的好内容变成可编辑、可检索、可长期复用的知识资产。

**官网：** [https://kb.apimar.online](https://kb.apimar.online)  
**注册 / 登录：** [https://kb.apimar.online/login](https://kb.apimar.online/login)  
**在线测试台：** [https://kb.apimar.online/playground](https://kb.apimar.online/playground)

---

## 一句话理解它

以前刷到好内容，你可能只是点个收藏；现在只要复制链接交给 FlowGate：

```text
短视频 / 图文链接
        ↓
自动解析媒体和作者信息
        ↓
语音转写 / 图片文字识别
        ↓
自动纠错、分段、补标点
        ↓
生成结构化 Markdown
        ↓
进入 Obsidian / 本地知识库 / RAG
```

> **每处理一条好内容，就相当于给自己的知识银行存入一笔资产。**

---

## 核心卖点

### 1. 5 分钟搭好自己的内容采集 Skill

不需要自己部署视频解析服务，不需要购买和配置语音识别模型，也不用安装一堆 Python 依赖。

你只需要完成三件事：

1. 把 Skill 放进 Claude Code；
2. 注册 FlowGate，复制 API Key；
3. 粘贴一条链接开始使用。

### 2. 一条链接，自动变成知识资产

提交公开链接后，FlowGate 会自动完成：

- 视频 / 图文平台识别；
- 标题、作者、封面、发布时间等元信息提取；
- 音视频语音转文字；
- 文本自动纠错、分段和标点补全；
- 图文笔记逐图文字识别；
- 生成统一的 Markdown 内容报告；
- 返回本次消耗与剩余积分。

### 3. 支持视频、图文、本地文件和批量表格

覆盖抖音、小红书、快手、哔哩哔哩、微博、TikTok、YouTube 等 80+ 平台。

- **口播视频：** 自动提取音频并生成干净文字稿；
- **图文笔记：** 自动逐图识别文字并汇总；
- **本地文件：** 支持录音、课程视频、播客等音视频；
- **批量表格：** 支持把 Excel / CSV 中的链接批量加工为知识库压缩包。

### 4. 输出可直接进入知识库

结果不是一段散乱文字，而是一份结构清晰的 Markdown：

```markdown
# 视频内容解析报告

## 基本信息
| 字段 | 内容 |
|---|---|
| 平台 | 抖音 |
| 标题 | …… |
| 作者 | …… |
| 发布时间 | …… |
| 原始链接 | …… |

## 内容
整理后的完整正文……

## 关键词 / 标签
- AI
- 内容生产
- 工作流
```

可以直接放进：

- Obsidian；
- Notion；
- 本地 Markdown 知识库；
- RAG / Agent 知识库；
- 选题库、案例库、竞品库；
- 自媒体内容生产工作流。

### 5. 成功才扣费，失败不计费

FlowGate 使用按量积分计费：

- 成功解析后按实际处理量结算；
- 解析失败不扣费；
- 每个账号拥有独立 API Key；
- 可查询余额和历史用量流水。

具体费率以官网和 `/pricing` 接口展示为准。

---

# 零基础配置教程

下面按顺序操作即可。整个过程通常只需要 5 分钟。

## 第 0 步：你需要准备什么？

安装前请确认电脑上已经有：

1. **Claude Code**：用于调用这个 Skill；
2. **Python 3**：用于运行内置客户端；
3. **FlowGate 账号**：用于获取 API Key；
4. 本项目的完整文件夹或压缩包。

检查 Python 是否安装：

### Windows PowerShell

```powershell
python --version
```

如果提示找不到 `python`，也可以试：

```powershell
py --version
```

### macOS / Linux

```bash
python3 --version
```

看到类似 `Python 3.10.12` 的版本号，就说明可以继续。

> 这个 Skill 只使用 Python 标准库，不需要执行 `pip install`。

---

## 第 1 步：注册并获取 API Key

1. 打开 [FlowGate 登录页](https://kb.apimar.online/login)；
2. 注册或登录账号；
3. 进入工作台；
4. 找到个人 **API Key**；
5. 点击复制并妥善保存。

API Key 通常是一段较长的密钥，例如：

```text
fg_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> 上面的内容只是格式示例，不是真实密钥。不要把自己的 API Key 发到群聊、截图、公开视频或 GitHub 仓库中。

还不想配置 Skill，也可以先打开 [在线测试台](https://kb.apimar.online/playground)，粘贴一条公开链接查看解析效果。

---

## 第 2 步：安装 Skill

推荐安装为 Claude Code 的个人 Skill，这样所有项目都能使用。

### 方法 A：解压后手动复制，适合新手

先解压下载的压缩包，确认目录中至少包含：

```text
flowgate-video/
├── SKILL.md
├── README.md
├── .env.example
├── scripts/
│   └── flowgate.py
└── references/
    └── api.md
```

然后把整个 `flowgate-video` 文件夹复制到 Claude Code 的个人 Skills 目录，并改名为 `flowgate-video-parser`。

#### Windows 目录

```text
C:\Users\你的用户名\.claude\skills\flowgate-video-parser\
```

也可以直接在文件资源管理器地址栏输入：

```text
%USERPROFILE%\.claude\skills
```

如果 `.claude` 或 `skills` 文件夹不存在，手动新建即可。

#### macOS / Linux 目录

```text
~/.claude/skills/flowgate-video-parser/
```

复制完成后，应当能看到：

```text
~/.claude/skills/flowgate-video-parser/SKILL.md
```

### 方法 B：使用命令复制

假设你已经进入包含 `flowgate-video` 文件夹的目录。

#### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force ".\flowgate-video" "$HOME\.claude\skills\flowgate-video-parser"
```

#### macOS / Linux

```bash
mkdir -p ~/.claude/skills
cp -R ./flowgate-video ~/.claude/skills/flowgate-video-parser
```

> 如果目标目录中已经有旧版本，建议先备份或删除旧文件夹，再复制新版。

---

## 第 3 步：填写 API Key

这是最关键的一步。

进入 Skill 文件夹，把 `.env.example` 复制为 `.env.local`，然后把你的 API Key 写进去。

### Windows PowerShell

```powershell
Set-Location "$HOME\.claude\skills\flowgate-video-parser"
Copy-Item ".env.example" ".env.local" -Force
notepad ".env.local"
```

### macOS / Linux

```bash
cd ~/.claude/skills/flowgate-video-parser
cp .env.example .env.local
nano .env.local
```

将文件内容修改为：

```env
FLOWGATE_API_KEY="你的真实 FlowGate API Key"
FLOWGATE_BASE_URL="https://kb.apimar.online"
FLOWGATE_OUTPUT_DIR="./reports"
```

例如：

```env
FLOWGATE_API_KEY="fg_abc123xxxxxxxxxxxxxxxx"
FLOWGATE_BASE_URL="https://kb.apimar.online"
FLOWGATE_OUTPUT_DIR="./reports"
```

三个配置项的作用：

| 配置项                | 是否必填 | 作用                                        |
| --------------------- | -------: | ------------------------------------------- |
| `FLOWGATE_API_KEY`    |       是 | 识别你的 FlowGate 账号并完成鉴权            |
| `FLOWGATE_BASE_URL`   |       否 | API 服务地址，通常保持默认即可              |
| `FLOWGATE_OUTPUT_DIR` |       否 | 未指定输出文件时，Markdown 默认保存到此目录 |

保存文件后关闭编辑器。

### Windows 常见坑：文件被保存成 `.env.local.txt`

Windows 记事本有时会自动加上 `.txt` 后缀。请在文件资源管理器中开启“显示文件扩展名”，确认文件名准确为：

```text
.env.local
```

而不是：

```text
.env.local.txt
```

### macOS / Linux 保存 nano 文件

在 nano 中：

1. 按 `Ctrl + O` 保存；
2. 按回车确认文件名；
3. 按 `Ctrl + X` 退出。

---

## 第 4 步：验证配置是否成功

先不要急着解析视频，运行余额查询最容易确认 API Key 是否有效。

### Windows PowerShell

```powershell
Set-Location "$HOME\.claude\skills\flowgate-video-parser"
python .\scripts\flowgate.py balance
```

如果你的电脑使用 `py` 命令：

```powershell
py .\scripts\flowgate.py balance
```

### macOS / Linux

```bash
cd ~/.claude/skills/flowgate-video-parser
python3 scripts/flowgate.py balance
```

配置正确时，会看到类似：

```text
余额：100 积分
```

如果看到：

```text
错误：未设置 API Key
```

请检查：

- `.env.local` 是否放在 `SKILL.md` 同级目录；
- 文件名是否被保存成 `.env.local.txt`；
- 配置项是否写成 `FLOWGATE_API_KEY=...`；
- 引号是否成对；
- API Key 前后是否有多余空格。

如果看到：

```text
错误：API Key 无效或缺失
```

请回到 FlowGate 工作台重新复制 API Key，替换旧值后再次运行。

---

## 第 5 步：完成第一次解析

找一条你有权处理的公开短视频或图文链接。

### 直接在 Claude Code 中使用

重启 Claude Code，或者重新打开一个会话，然后输入：

```text
帮我解析这个视频，并保存成 Markdown：
https://v.douyin.com/xxxxx/
```

也可以说得更具体：

```text
调用 FlowGate Video Parser，把这个小红书图文整理成 Markdown，保留标题、作者、原链接、正文和关键词：
https://www.xiaohongshu.com/explore/xxxxx
```

### 用命令行测试

#### Windows PowerShell

```powershell
python .\scripts\flowgate.py transcribe "https://v.douyin.com/xxxxx/" --output ".\reports\first-note.md"
```

#### macOS / Linux

```bash
python3 scripts/flowgate.py transcribe "https://v.douyin.com/xxxxx/" --output "./reports/first-note.md"
```

成功后会显示：

```text
报告已保存：reports/first-note.md
本次扣费 N 积分 · 剩余余额 M
```

打开 `reports/first-note.md`，你就完成了第一笔“知识存款”。

---

## 第 6 步：把结果存进 Obsidian

最简单的方式，是把默认输出目录直接设置到 Obsidian Vault 中。

例如你的 Obsidian 收件箱目录是：

### Windows

```text
D:\MyObsidian\KnowledgeBase\Inbox
```

把 `.env.local` 中的配置改成：

```env
FLOWGATE_OUTPUT_DIR="D:/MyObsidian/KnowledgeBase/Inbox"
```

### macOS

```text
/Users/你的用户名/Documents/Obsidian/KnowledgeBase/Inbox
```

配置为：

```env
FLOWGATE_OUTPUT_DIR="/Users/你的用户名/Documents/Obsidian/KnowledgeBase/Inbox"
```

以后不传 `--output` 时，生成的 Markdown 会直接进入这个文件夹：

```bash
python3 scripts/flowgate.py transcribe "视频链接"
```

建议在 Obsidian 中建立：

```text
KnowledgeBase/
├── 00-Inbox/          # 新解析、待整理
├── 10-Topics/         # 按主题沉淀
├── 20-Cases/          # 案例与竞品
├── 30-Ideas/          # 选题和灵感
└── 90-Archive/        # 原始内容归档
```

---

# 三种 API Key 配置方式

普通用户推荐使用第一种。

## 方式一：`.env.local`，最推荐

把 `.env.local` 放在 `SKILL.md` 同级目录：

```text
flowgate-video-parser/
├── SKILL.md
├── .env.local
└── scripts/
```

优点：长期有效、配置简单、不需要每次输入密钥。

## 方式二：系统环境变量

适合熟悉终端的用户。

### Windows PowerShell，当前窗口有效

```powershell
$env:FLOWGATE_API_KEY="你的 API Key"
```

### Windows PowerShell，写入用户环境变量

```powershell
[Environment]::SetEnvironmentVariable("FLOWGATE_API_KEY", "你的 API Key", "User")
```

执行后重新打开终端和 Claude Code。

### macOS / Linux，当前终端有效

```bash
export FLOWGATE_API_KEY="你的 API Key"
```

长期生效可写入 `~/.zshrc` 或 `~/.bashrc`：

```bash
export FLOWGATE_API_KEY="你的 API Key"
```

然后执行：

```bash
source ~/.zshrc
```

## 方式三：命令行临时传入

```bash
python scripts/flowgate.py balance --api-key "你的 API Key"
```

这种方式适合临时测试，不建议长期使用，因为密钥可能出现在终端历史记录中。

---

# 安装为当前项目的 Skill

只想让某个项目使用时，可以放在项目内部：

```text
你的项目/
└── .claude/
    └── skills/
        └── flowgate-video-parser/
            ├── SKILL.md
            ├── .env.local
            ├── scripts/
            └── references/
```

项目级 Skill 适合：

- 团队项目采用统一的内容采集流程；
- 希望输出固定到项目的资料目录；
- 不想让其他 Claude Code 项目自动调用该 Skill。

> 提交 Git 仓库前，请务必把 `.env.local` 加入 `.gitignore`。

建议在 `.gitignore` 中加入：

```gitignore
.env
.env.local
reports/
```

---

# 日常怎么使用？

## 场景一：解析短视频

```text
把这个抖音视频转成 Markdown，保留基本信息、完整正文和关键词：
https://v.douyin.com/xxxxx/
```

## 场景二：解析小红书图文

```text
识别这篇小红书图文中的所有文字，整理为结构化 Markdown，并提取核心观点：
https://www.xiaohongshu.com/explore/xxxxx
```

## 场景三：解析 B 站长视频

```text
把这个 B 站视频转成完整文字稿，并按主题分段：
https://www.bilibili.com/video/BVxxxxxxxxx
```

## 场景四：沉淀为知识卡片

```text
先调用 FlowGate 解析链接，再把结果提炼成一张知识卡片，包含：一句话结论、核心观点、案例、可执行动作和原始链接。
```

## 场景五：生成内容选题

```text
解析这个视频，然后基于其中的观点生成 10 个小红书选题。不要照抄原文，保留来源链接。
```

---

# 命令行使用

即使不使用 Claude Code，也可以直接调用内置 CLI。

## 1. 解析一条视频 / 图文链接

```bash
python scripts/flowgate.py transcribe "https://v.douyin.com/xxxxx/" --output report.md
```

macOS / Linux 通常使用：

```bash
python3 scripts/flowgate.py transcribe "https://v.douyin.com/xxxxx/" --output report.md
```

常用参数：

```bash
# 只解析元信息和媒体地址，不做语音转写
python scripts/flowgate.py transcribe "链接" --no-transcribe

# 输出完整 JSON，方便程序继续处理
python scripts/flowgate.py transcribe "链接" --json

# 指定 Markdown 保存位置
python scripts/flowgate.py transcribe "链接" --output reports/demo.md

# 长视频增加请求超时时间
python scripts/flowgate.py transcribe "链接" --timeout 1200
```

## 2. 转写本地音视频文件

支持常见音频和视频格式，包括 mp3、m4a、wav、ogg、flac、mp4、mov、mkv、webm 等。

```bash
python scripts/flowgate.py transcribe-file "C:/path/to/lecture.mp4" --output lecture.md
```

macOS / Linux：

```bash
python3 scripts/flowgate.py transcribe-file "/Users/name/lecture.mp4" --output lecture.md
```

长音视频会在服务端自动抽取音频、分片转写并重新合并。

## 3. 批量解析 Excel / CSV

表格需要包含以下任意一种链接列名：

```text
作品链接 / 笔记链接 / 视频链接 / 链接 / url / 作品url
```

示例：

| 标题          | 作者 | 作品链接                                  |
| ------------- | ---- | ----------------------------------------- |
| AI 工作流分享 | 张三 | https://v.douyin.com/xxxxx/               |
| 内容生产方法  | 李四 | https://www.xiaohongshu.com/explore/xxxxx |

提交批量任务并等待完成：

```bash
python scripts/flowgate.py batch works.xlsx
```

只提交任务，不等待：

```bash
python scripts/flowgate.py batch works.xlsx --no-wait
```

查看任务列表：

```bash
python scripts/flowgate.py batch-list
```

查询任务并下载知识库：

```bash
python scripts/flowgate.py batch-status BAT2026xxxx --download
```

批量任务完成后会生成：

```text
knowledge_base_<batch_no>.zip
├── notes/
│   ├── 001_内容标题.md
│   ├── 002_内容标题.md
│   └── ...
├── index.md
└── summary.xlsx
```

每一条成功内容单独计费，失败内容不计费；失败行会自动重试一次。

## 4. 查询账户信息

```bash
# 查询积分余额
python scripts/flowgate.py balance

# 查询最近 20 条用量流水
python scripts/flowgate.py usage --limit 20

# 使用卡密充值
python scripts/flowgate.py redeem <卡密>
```

---

# 一个真实的知识银行工作流

## 日常采集

刷到有价值的短视频或图文时：

1. 复制公开链接；
2. 发给 Claude Code；
3. FlowGate 自动生成 Markdown；
4. 保存到 `Inbox` 或 `待整理` 文件夹。

## 自动整理

再让 Agent 继续完成：

- 提取核心观点；
- 生成摘要和关键词；
- 判断内容所属主题；
- 与已有笔记建立双向链接；
- 提炼成知识卡片；
- 加入选题库或案例库；
- 生成公众号、小红书或视频脚本初稿。

## 长期复利

```text
信息流
  ↓
原始内容资产
  ↓
结构化知识卡片
  ↓
选题 / 案例 / 方法论
  ↓
文章 / 视频 / 产品 / 决策
```

FlowGate 解决的不是“下载一条视频”，而是打通：

> **信息消费 → 自动沉淀 → 知识复用 → 内容生产**

---

# 常见报错与解决办法

## 1. `未设置 API Key`

原因：程序没有读取到 `FLOWGATE_API_KEY`。

解决：

1. 确认文件名是 `.env.local`；
2. 确认它和 `SKILL.md` 位于同一文件夹；
3. 确认内容不是示例值；
4. 重新运行 `balance`。

## 2. `API Key 无效或缺失` / HTTP 401

原因：API Key 复制不完整、已失效，或者多复制了空格。

解决：重新登录 FlowGate 工作台，完整复制 API Key 后替换。

## 3. `积分余额不足` / HTTP 402

原因：当前积分不足以完成任务。

解决：充值或兑换卡密，然后运行：

```bash
python scripts/flowgate.py redeem <卡密>
```

## 4. `解析失败` / HTTP 502

可能原因：

- 链接已失效；
- 内容不是公开内容；
- 平台临时限制访问；
- 视频或图集正在审核、删除或下架；
- 网络或上游服务暂时异常。

失败任务不扣费。可以稍后重试，或者更换一条公开链接。

## 5. `python 不是内部或外部命令`

Windows 可以尝试：

```powershell
py .\scripts\flowgate.py balance
```

如果 `python` 和 `py` 都不可用，需要先安装 Python 3，并在安装时勾选 **Add Python to PATH**。

## 6. 找不到 `scripts/flowgate.py`

原因：当前终端不在 Skill 文件夹中。

Windows：

```powershell
Set-Location "$HOME\.claude\skills\flowgate-video-parser"
```

macOS / Linux：

```bash
cd ~/.claude/skills/flowgate-video-parser
```

然后再运行命令。

## 7. Claude Code 没有自动调用 Skill

请检查：

- 目录中是否存在 `SKILL.md`；
- 文件是否位于 `~/.claude/skills/flowgate-video-parser/`；
- 是否已经重启 Claude Code 或重新打开会话；
- 提示词是否明确包含“解析视频链接、转写、生成 Markdown”等意图。

也可以直接说：

```text
请调用 flowgate-video-parser Skill 处理下面的链接。
```

## 8. 报告没有保存到预期目录

请检查 `.env.local` 中的：

```env
FLOWGATE_OUTPUT_DIR="./reports"
```

相对路径是相对于你运行命令时所在的目录。为了避免混淆，可以改成绝对路径。

---

# 安全提醒

## 不要泄露 API Key

请勿：

- 把 `.env.local` 上传到 GitHub；
- 在截图、录屏或教程中展示完整 API Key；
- 把 API Key 写进公开网页前端；
- 把密钥直接硬编码到公开脚本。

如果怀疑密钥已经泄露，请尽快在工作台更新或更换密钥。

## 只处理有权使用的公开内容

请尊重平台规则、版权和内容授权：

- 仅处理公开内容；
- 不绕过登录、付费或访问限制；
- 不将工具用于未经授权的搬运、侵权传播或商业再发布；
- 对解析结果的使用、发布和版权合规由使用者自行负责；
- 平台名称及商标归各自权利人所有，FlowGate 与相关平台不存在隶属、赞助或授权关系。

---

# 项目结构

```text
flowgate-video-parser/
├── SKILL.md               # Skill 入口与 Agent 工作流说明
├── README.md              # 中文安装与使用教程
├── .env.example           # 环境变量示例
├── scripts/
│   └── flowgate.py        # 纯 Python 标准库 CLI 客户端
├── references/
│   └── api.md             # API 接口、字段、错误码与计费说明
├── LICENSE
└── NOTICE
```

---

# API 简介

默认服务地址：

```text
https://kb.apimar.online
```

鉴权方式：

```http
Authorization: Bearer <FLOWGATE_API_KEY>
```

核心接口：

| 接口                       | 用途                          |
| -------------------------- | ----------------------------- |
| `POST /v1/transcribe`      | 解析并转写公开视频 / 图文链接 |
| `POST /v1/transcribe-file` | 上传并转写本地音视频文件      |
| `POST /v1/batch`           | 批量提交 Excel / CSV          |
| `GET /v1/batch`            | 查询批量任务列表              |
| `GET /v1/balance`          | 查询积分余额                  |
| `GET /v1/usage`            | 查询用量流水                  |
| `POST /v1/redeem`          | 使用卡密充值                  |
| `GET /pricing`             | 查询当前积分费率              |

完整字段与错误码请查看 [`references/api.md`](references/api.md)。

---

# 常见问题

## 是否需要自己部署解析器或 ASR 模型？

不需要。媒体解析、语音转写、文本纠错和图像识别都由 FlowGate 托管服务完成，本地只负责提交任务和接收结果。

## 是否需要安装第三方 Python 包？

不需要。`scripts/flowgate.py` 使用 Python 标准库实现，通常无需运行 `pip install`。

## 解析失败会扣积分吗？

不会。只有成功返回结果时才计费，解析失败不扣费。

## 可以处理私密、付费或需要登录的内容吗？

不可以。请仅处理公开且你依法拥有权利或已获得授权的内容。FlowGate 不绕过登录墙、付费墙或其他访问控制。

## 转写一定完全准确吗？

清晰口播通常效果较好，但强背景音乐、方言、多人重叠发言、低音质录音可能产生误差。重要内容建议人工复核。

## 可以直接接入 Obsidian 吗？

可以。把 `FLOWGATE_OUTPUT_DIR` 设置为 Obsidian Vault 中的某个文件夹即可。批量任务还会生成每条内容独立的 Markdown、索引文件和汇总表格。

## API Key 应该放在哪里？

推荐放在 Skill 目录中的 `.env.local`，也可以使用系统环境变量 `FLOWGATE_API_KEY`。不要把密钥写入公开仓库。

---

# License

本项目采用 [Apache License 2.0](LICENSE) 开源许可证。

---

## 现在开始给知识银行“存钱”

1. 注册并获取 API Key；
2. 把 Skill 复制到 Claude Code；
3. 在 `.env.local` 中填入密钥；
4. 运行 `balance` 检查配置；
5. 复制一条有价值的短视频或图文链接；
6. 把它变成真正属于你的知识资产。

**FlowGate：一条链接，视频图文一键成稿。**
