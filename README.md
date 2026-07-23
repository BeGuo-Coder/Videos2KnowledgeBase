# Videos2KnowledgeBase
https://kb.apimar.online/
FlowGate Video Parser Skill

5 分钟搭好一个内容采集 Skill。从此，刷短视频不只是消费内容，而是在给你的知识银行持续“存钱”。

FlowGate Video Parser 是一个面向 Claude Code / Agent 的轻量级 Skill。你只需要丢给它一条公开的短视频或图文链接，它就能自动完成媒体解析、语音转写、图像文字识别、文本纠错和 Markdown 整理，把稍纵即逝的信息流变成可编辑、可检索、可长期复用的知识资产。

官网： https://kb.apimar.online注册并获取 API Key： https://kb.apimar.online/login

为什么要做这个 Skill？

我们每天会刷到大量有价值的内容：行业观点、产品案例、商业模式、教程、选题灵感、竞品分析……

但大多数内容只是：

看过了，却没有留下来；

收藏了，却再也没有打开；

想整理，却没有时间手动下载、听写和归档；

真正需要时，已经找不到原视频。

FlowGate 把这条链路变成一个自动化动作：

看到有价值的内容
        ↓
复制视频 / 图文链接
        ↓
交给 FlowGate Skill
        ↓
自动解析、转写、识别、纠错
        ↓
生成结构化 Markdown 报告
        ↓
进入 Obsidian / Notion / 本地知识库

从此：

每刷到一条好内容，就给自己的知识银行存入一笔资产。

核心卖点

1. 5 分钟搭好自己的内容采集 Skill

不需要部署视频解析服务，不需要配置语音识别模型，也不需要安装一堆 Python 依赖。

你只需要：

把 Skill 放进 Claude Code；

注册 FlowGate，获取 API Key；

粘贴一条链接开始使用。

客户端仅使用 Python 标准库，开箱即用。

2. 一条链接，自动变成知识资产

提交公开链接后，FlowGate 会自动完成：

视频 / 图文平台识别；

标题、作者、封面、发布时间等元信息提取；

音视频语音转文字；

文本自动纠错与标点补全；

图文笔记逐图文字识别；

统一生成 Markdown 内容报告；

返回本次消耗与剩余积分。

3. 支持短视频，也支持图文笔记

覆盖抖音、小红书、快手、哔哩哔哩、微博、TikTok、YouTube 等 80+ 平台。

口播视频： 自动提取音频并转成干净文字稿；

图文笔记： 自动逐图识别文字并汇总；

本地文件： 可上传录音、课程视频、播客等音视频文件；

批量表格： 可把 Excel / CSV 中的链接批量加工为知识库压缩包。

4. 不只是转写，而是直接入库

输出不是一段散乱文字，而是一份结构清晰的 Markdown 报告：

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

可以直接放进：

Obsidian；

Notion；

本地 Markdown 知识库；

RAG / Agent 知识库；

选题库、案例库、竞品库；

自媒体内容生产工作流。

5. 成功才扣费，失败不计费

FlowGate 使用按量积分计费：

成功解析后按实际处理量结算；

解析失败不扣费；

每个账号拥有独立 API Key；

可随时查询余额和历史用量流水。

具体费率以官网和 /pricing 接口展示为准。

适合谁使用？

内容创作者

把爆款视频、优秀图文和选题灵感自动沉淀为素材库，为小红书、公众号、短视频脚本和课程内容提供原始素材。

AI 知识库用户

把信息流中的零散内容转成标准 Markdown，持续写入 Obsidian、Hermes、本地 RAG 或个人知识图谱。

产品经理与创业者

批量收集行业案例、竞品动态、用户痛点和商业模式，形成可检索的市场情报库。

学习者与研究者

把课程、访谈、播客、演讲和知识类视频转成文字资料，便于总结、搜索、引用和复习。

开发者与 Agent 构建者

通过 API 或现成 CLI，把视频图文解析能力快速接入自己的 Agent、自动化工作流或内容产品。

5 分钟快速安装

方式一：安装为 Claude Code 个人 Skill

个人 Skill 会对你的所有项目生效。

macOS / Linux

mkdir -p ~/.claude/skills
cp -R flowgate-video ~/.claude/skills/flowgate-video-parser
cd ~/.claude/skills/flowgate-video-parser
cp .env.example .env.local

Windows PowerShell

New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse ".\flowgate-video" "$HOME\.claude\skills\flowgate-video-parser"
Set-Location "$HOME\.claude\skills\flowgate-video-parser"
Copy-Item ".env.example" ".env.local"

然后编辑 .env.local：

FLOWGATE_API_KEY="你的 FlowGate API Key"
FLOWGATE_BASE_URL="https://kb.apimar.online"
FLOWGATE_OUTPUT_DIR="./reports"

获取 API Key：

打开 FlowGate；

注册或登录账号；

在工作台复制个人 API Key；

填入 .env.local。

请勿把 .env.local 或 API Key 提交到 Git 仓库，也不要在公开聊天中展示密钥。

方式二：安装为项目 Skill

只想让当前项目使用时，将目录复制到项目内：

你的项目/
└── .claude/
    └── skills/
        └── flowgate-video-parser/
            ├── SKILL.md
            ├── scripts/
            ├── references/
            └── .env.local

开始使用

启动 Claude Code 后，可以直接用自然语言：

帮我解析这个视频，并保存成 Markdown：
https://v.douyin.com/xxxxx/

也可以直接调用 Skill：

/flowgate-video-parser https://v.douyin.com/xxxxx/

你还可以这样说：

把这个小红书图文笔记识别成 Markdown，并提取关键词。

把这个 B 站视频转成完整文字稿，保留标题、作者和原始链接。

将这份 Excel 中的作品链接批量解析，并打包成 Obsidian 知识库。

命令行使用

即使不使用 Claude Code，也可以直接调用内置 CLI。

1. 解析一条视频 / 图文链接

python scripts/flowgate.py transcribe "https://v.douyin.com/xxxxx/" --output report.md

常用参数：

# 只解析元信息和媒体地址，不做语音转写
python scripts/flowgate.py transcribe "链接" --no-transcribe

# 输出完整 JSON，方便程序继续处理
python scripts/flowgate.py transcribe "链接" --json

# 指定 Markdown 保存位置
python scripts/flowgate.py transcribe "链接" --output reports/demo.md

2. 转写本地音视频文件

支持常见音频和视频格式，包括 mp3、m4a、wav、ogg、flac、mp4、mov、mkv、webm 等。

python scripts/flowgate.py transcribe-file "C:/path/to/lecture.mp4" --output lecture.md

长音视频会在服务端自动抽取音频、分片转写并重新合并。

3. 批量解析 Excel / CSV

表格需要包含以下任意一种链接列名：

作品链接 / 笔记链接 / 视频链接 / 链接 / url / 作品url

提交批量任务并等待完成：

python scripts/flowgate.py batch works.xlsx

只提交任务，不等待：

python scripts/flowgate.py batch works.xlsx --no-wait

查看任务列表：

python scripts/flowgate.py batch-list

查询任务并下载知识库：

python scripts/flowgate.py batch-status BAT2026xxxx --download

批量任务完成后会生成：

knowledge_base_<batch_no>.zip
├── notes/
│   ├── 001_内容标题.md
│   ├── 002_内容标题.md
│   └── ...
├── index.md
└── summary.xlsx

每一条成功内容单独计费，失败内容不计费；失败行会自动重试一次。

4. 查询账户信息

# 查询积分余额
python scripts/flowgate.py balance

# 查询最近 20 条用量流水
python scripts/flowgate.py usage --limit 20

# 使用卡密充值
python scripts/flowgate.py redeem <卡密>

一个真实的知识银行工作流

日常采集

刷到有价值的短视频或图文时：

复制公开链接；

发给 Claude Code；

FlowGate 自动生成 Markdown；

保存到 Inbox 或 待整理 文件夹。

自动整理

再让 Agent 继续完成：

提取核心观点；

生成摘要和关键词；

判断内容所属主题；

与已有笔记建立双向链接；

提炼成知识卡片；

加入选题库或案例库；

生成公众号、小红书或视频脚本初稿。

长期复利

信息流
  ↓
原始内容资产
  ↓
结构化知识卡片
  ↓
选题 / 案例 / 方法论
  ↓
文章 / 视频 / 产品 / 决策

FlowGate 解决的不是“下载一条视频”，而是打通：

信息消费 → 自动沉淀 → 知识复用 → 内容生产

项目结构

flowgate-video-parser/
├── SKILL.md               # Skill 入口与 Agent 工作流说明
├── README.md              # 中文使用说明
├── .env.example           # 环境变量示例
├── scripts/
│   └── flowgate.py        # 纯 Python 标准库 CLI 客户端
├── references/
│   └── api.md             # API 接口、字段、错误码与计费说明
├── LICENSE
└── NOTICE

API 简介

默认服务地址：

https://kb.apimar.online

鉴权方式：

Authorization: Bearer <FLOWGATE_API_KEY>

核心接口：

接口

用途

POST /v1/transcribe

解析并转写公开视频 / 图文链接

POST /v1/transcribe-file

上传并转写本地音视频文件

POST /v1/batch

批量提交 Excel / CSV

GET /v1/batch

查询批量任务列表

GET /v1/balance

查询积分余额

GET /v1/usage

查询用量流水

POST /v1/redeem

使用卡密充值

GET /pricing

查询当前积分费率

完整字段与错误码请查看 references/api.md。

常见问题

是否需要自己部署解析器或 ASR 模型？

不需要。媒体解析、语音转写、文本纠错和图像识别都由 FlowGate 托管服务完成，本地只负责提交任务和接收结果。

是否需要安装第三方 Python 包？

不需要。scripts/flowgate.py 使用 Python 标准库实现，通常无需运行 pip install。

解析失败会扣积分吗？

不会。只有成功返回结果时才计费，解析失败不扣费。

可以处理私密、付费或需要登录的内容吗？

不可以。请仅处理公开且你依法拥有权利或已获得授权的内容。FlowGate 不绕过登录墙、付费墙或其他访问控制。

转写一定完全准确吗？

清晰口播通常效果较好，但强背景音乐、方言、多人重叠发言、低音质录音可能产生误差。重要内容建议人工复核。

可以直接接入 Obsidian 吗？

单条任务可以直接输出 Markdown；批量任务会生成每条内容独立的 Markdown、索引文件和汇总表格，可解压后放入 Obsidian Vault。

API Key 应该放在哪里？

推荐放在 Skill 目录旁的 .env.local 中，也可以通过系统环境变量 FLOWGATE_API_KEY 配置。不要把密钥写入公开仓库。

合规说明

请尊重平台规则、版权和内容授权：

仅处理公开内容；

不绕过登录、付费或访问限制；

不将本工具用于未经授权的搬运、侵权传播或商业再发布；

对解析结果的使用、发布和版权合规由使用者自行负责；

平台名称及商标归各自权利人所有，FlowGate 与相关平台不存在隶属、赞助或授权关系。

License

本项目采用 Apache License 2.0 开源许可证。

现在开始给知识银行“存钱”

注册并获取 API Key；

安装 Skill；

复制一条有价值的短视频或图文链接；

把它变成真正属于你的知识资产。

FlowGate：一条链接，视频图文一键成稿。
