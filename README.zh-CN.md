# awesome-ai-image-prompts

**🌍 [English](README.md) · [简体中文](README.zh-CN.md) · [Bahasa Melayu](README.ms.md)**

> **Prompt-as-Code 提示词代码库** — 955 条精选 AI 图像生成提示词，
> 适配 GPT-Image-2、Nano Banana、Seedance、Qwen-VL、Gemini Imagen 等多模型。
> Apache 2.0 协议。多语言 (zh / en / ms)。**开箱即用的 RAG 检索。**

[![License](https://img.shields.io/badge/code-Apache%202.0-blue.svg)](LICENSE)
[![Prompts](https://img.shields.io/badge/prompts-955-green.svg)](data/prompts.json)
[![Languages](https://img.shields.io/badge/languages-zh%20%7C%20en%20%7C%20ms-orange.svg)](#多语言)

---

## 这是什么

一个**可检索**的 AI 图像生成提示词库，从公开来源精选并附带**逐条 attribution 与
license 元数据**。跟传统 awesome-* 提示词列表不同，本仓库提供：

- **955 条 prompt**，结构化 JSON schema（非 markdown 流水账）
- **逐条质量分** (1–10)，检索时可按层级筛选
- **多语言元数据** (zh / en / ms)
- **完整可运行的 RAG pipeline** (Qdrant + e5 embedding)，clone 后 5 分钟可用
- **BYOP 摄入脚手架**，方便接入你自己的提示词集

仓库**模型无关**。这些 prompt 适用于 GPT-Image-2（原始目标）、Google Nano Banana、
Seedance、Qwen-VL、Gemini Imagen，以及任何强 text-to-image 模型。

## 为什么再造一个提示词库？

大多数 "awesome-*" 提示词列表是 markdown 画廊堆栈 — 看着好看，集成困难。这个仓库
设计为**给 agent 调用**：

```python
from tools.prompt_rag import find_similar
hits = find_similar("商务女性介绍产品", k=3)
# → [{'title': '珊瑚色极简影棚时尚商业大片', 'score': 8, 'prompt': '...', 'author': '@...'}, ...]
```

把 `hits` 直接塞进你的 Qwen / GPT / Claude 系统提示词作 few-shot examples，
出图质量明显跃升。

## 快速上手

```bash
git clone https://github.com/NeXra-AI/awesome-ai-image-prompts.git
cd awesome-ai-image-prompts
pip install -r tools/requirements.txt

# 首次：建本地 Qdrant 索引（首跑下载 ~1.5GB e5 模型）
python tools/search_cli.py --index

# 之后搜索：
python tools/search_cli.py "cyberpunk product shot, neon, night"
python tools/search_cli.py "电商海报 中国风 红色" --k 5 --min-score 8
```

输出：

```
  Query: 电商海报 中国风 红色
  Found 3 reference prompts

1. [8/10] 红蓝光影下的未来都市双重曝光青年  (similarity 0.872)
   by Fujimoto_hina | Attribution Required (X.com public post)
   source: https://x.com/Fujimoto_hina/status/...
   一位年轻男子的超写实电影级双重曝光侧脸肖像...
```

## 仓库结构

```
awesome-ai-image-prompts/
├── data/
│   ├── prompts.json     # 955 条结构化数据
│   └── images/          # 953 张参考图
├── tools/
│   ├── prompt_rag.py    # Qdrant + e5 RAG pipeline
│   ├── search_cli.py    # 一行命令搜索
│   ├── ingest_skeleton.py  # BYOP 脚手架
│   └── requirements.txt
├── scripts/
│   └── export_from_nexra.py  # 数据集组装脚本
├── LICENSE              # Apache 2.0 (代码)
├── NOTICE               # 必要 attribution
└── ATTRIBUTION.md       # 各来源 license 详情
```

## 数据 Schema

每条 `data/prompts.json` 条目：

```jsonc
{
  "id": "awgi2-469",
  "title": "导览式科普绘本",
  "title_en": "...", "title_zh": "...", "title_ms": "...",
  "prompt": "请根据【主题】创作一张高完成度的「导览式科普绘本」风格插画...",
  "prompt_zh": "...", "prompt_ms": "...",
  "category": "illustration",
  "image_url": "data/images/awgi2-469.jpg",
  "source": "awesome-gpt-image-2",
  "source_url": "https://x.com/MrLarus/status/...",
  "author": "MrLarus",
  "license": "Attribution Required (X.com public post)",
  "lang": "zh",
  "quality_score": 8,
  "seo_keywords": { "en": [...], "zh": [...], "ms": [...] }
}
```

## 协议与署名

- **`tools/` 和 `scripts/` 中的代码**：Apache 2.0 (LICENSE + NOTICE)
- **`data/prompts.json` 中的 prompt**：逐条 license 写在 `license` 字段

**完整来源协议详情见 [ATTRIBUTION.md](ATTRIBUTION.md)**。再分发时
**必须保留 `author`、`source`、`source_url`、`license` 字段** — 这是规则。

## 多语言

所有条目带 `title_en` / `title_zh` / `title_ms` 以及 `prompt_zh` / `prompt_ms`
（已翻译的）。用途：

- UI 按用户语言显示 prompt 建议
- 按用户偏好语言搜索
- 跨语言 RAG 查询（e5 模型支持跨语 embedding 匹配）

## BYOP (Bring Your Own Prompts)

`tools/ingest_skeleton.py` 展示了 schema 与去重模式。把 `normalise_entry()`
适配到你的输入格式后：

```python
from tools.ingest_skeleton import normalise_entry, merge_into_library
entries = [normalise_entry(r, source_name="my_team", default_license="MIT") for r in my_data]
merge_into_library(entries)
```

重跑 `python tools/search_cli.py --index` 刷新索引。

---

## 配合 AI Agent 使用

最佳搭档：**[NeXra Agent CLI](https://github.com/NeXra-AI/agent-cli)** — agent
从本库挑选参考 prompt、调 t2i 模型、处理计费、推送到你的渠道：

```bash
nexra prompt search "电商海报 中国风" --generate --model qwen
```

你也可以 fork 本仓库接入任何 agent runtime（Claude Code、Cursor、自家的）。
检索 API 就 `find_similar()` 一个函数。

## 本仓库 vs NeXra 平台的区别

本仓库 ship 的是 **license 干净的子集**。完整 NeXra 平台还包含：

- **1664+ prompts**（全库，含按 fair use + attribution 展示的不开源条目）
- **一键生图**，集成计费（5+ 模型可选）
- **Agent CLI** (`nexra prompt search → generate → publish`)
- **14+ 营销集成**（Meta Ads / WhatsApp / Stripe / Shopee / ...）
- **垂直行业 pack**：餐饮 / 零售 / 房产 / 电商

觉得有用见 [nexra-ai.co](https://nexra-ai.co)。不需要的话欢迎 fork 自建 —
这正是开源的意义。

## 路线图

- [ ] embedding 模型可切换（bge-m3 / jina-v3 等更小更快）
- [ ] 静态 HTML 画廊生成器（不 clone 也能浏览）
- [ ] Web embedding playground
- [ ] prompt 质量评分细则文档
- [ ] 更多垂直领域（美食摄影、时尚目录、房产）

## 参与贡献

提 issue 接受：
- **下架请求**（如果你是原作者）
- **新源提议**（请带清晰 license 证据）
- **质量问题**（评分错、分类错、图坏）

PR 欢迎（`tools/`、`scripts/`）。

## 致谢

特别鸣谢以下精选合集策展人：
[freestylefly](https://github.com/freestylefly/awesome-gpt-image-2)、
[EvoLinkAI](https://github.com/EvoLinkAI)、
[jamez-bondos](https://github.com/jamez-bondos/awesome-gpt4o-images)，
以及 X.com 上 200+ 原始 prompt 作者。完整名单见 [ATTRIBUTION.md](ATTRIBUTION.md)。
