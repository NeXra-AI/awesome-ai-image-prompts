# awesome-ai-image-prompts

**🌍 [English](README.md) · [简体中文](README.zh-CN.md) · [Bahasa Melayu](README.ms.md)**

> **Prompt-as-Code library** — 955 curated prompts for GPT-Image-2, Nano Banana,
> Seedance, Qwen-VL, Gemini Imagen, and more.
> Apache 2.0. Multi-language (zh / en / ms). **RAG-ready out of the box.**

[![License](https://img.shields.io/badge/code-Apache%202.0-blue.svg)](LICENSE)
[![Prompts](https://img.shields.io/badge/prompts-955-green.svg)](data/prompts.json)
[![Languages](https://img.shields.io/badge/languages-zh%20%7C%20en%20%7C%20ms-orange.svg)](#multi-language)

---

## What this is

A retrievable prompt library for AI image generation, distilled from public
sources with **per-entry attribution and licensing**. Unlike static prompt
lists, this repo ships:

- **955 prompts** in a structured JSON schema (not free-form markdown)
- **Per-entry quality scores** (1–10) so retrieval can filter by tier
- **Multi-language metadata** (zh / en / ms)
- **A working RAG pipeline** (Qdrant + e5 embedding) — clone and search in 5 minutes
- **BYOP-friendly ingest scaffolding** for adding your own prompts

The repo is **model-agnostic**. The prompts work with GPT-Image-2 (the original
target), Google Nano Banana, Seedance, Qwen-VL, Gemini Imagen, and any other
strong text-to-image model.

## Why another prompt repo?

Most "awesome-*" prompt lists are markdown gallery dumps — pretty to look at,
hard to integrate. This one is built to be **called by an agent**:

```python
from tools.prompt_rag import find_similar
hits = find_similar("商务女性介绍产品", k=3)
# → [{'title': '珊瑚色极简影棚时尚商业大片', 'score': 8, 'prompt': '...', 'author': '@...'}, ...]
```

Drop those `hits` straight into your Qwen / GPT / Claude prompt as few-shot
examples, and image quality jumps materially.

## Quick start

```bash
git clone https://github.com/<owner>/awesome-ai-image-prompts.git
cd awesome-ai-image-prompts
pip install -r tools/requirements.txt

# One-time: build the local Qdrant index (first run downloads ~1.5GB e5 model)
python tools/search_cli.py --index

# Now search:
python tools/search_cli.py "cyberpunk product shot, neon, night"
python tools/search_cli.py "电商海报 中国风 红色" --k 5 --min-score 8
```

Output:

```
  Query: 电商海报 中国风 红色
  Found 3 reference prompts

1. [8/10] 红蓝光影下的未来都市双重曝光青年  (similarity 0.872)
   by Fujimoto_hina | Attribution Required (X.com public post)
   source: https://x.com/Fujimoto_hina/status/...
   一位年轻男子的超写实电影级双重曝光侧脸肖像...
```

## Repo structure

```
awesome-ai-image-prompts/
├── data/
│   ├── prompts.json     # 955 entries, structured schema
│   └── images/          # 953 reference images
├── tools/
│   ├── prompt_rag.py    # Qdrant + e5 RAG pipeline
│   ├── search_cli.py    # one-liner search
│   ├── ingest_skeleton.py  # BYOP scaffolding
│   └── requirements.txt
├── scripts/
│   └── export_from_nexra.py  # how this corpus was assembled
├── LICENSE              # Apache 2.0 (code)
├── NOTICE               # required attributions
└── ATTRIBUTION.md       # per-source license breakdown
```

## Data schema

Each entry in `data/prompts.json`:

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

## Licensing & attribution

- **Code** in `tools/` and `scripts/`: Apache 2.0 (LICENSE + NOTICE)
- **Prompts** in `data/prompts.json`: per-entry license in the `license` field

See **[ATTRIBUTION.md](ATTRIBUTION.md)** for the full breakdown by source.
**Always preserve `author`, `source`, `source_url`, `license`** when
redistributing. That's the deal.

## Multi-language

All entries carry `title_en` / `title_zh` / `title_ms` and `prompt_zh` /
`prompt_ms` where available. Useful for:

- Localized prompt suggestions in your UI
- Searching by user's preferred language
- Multi-language RAG queries (the e5 model handles cross-lingual matching)

## Bring Your Own Prompts (BYOP)

`tools/ingest_skeleton.py` shows the schema and dedupe pattern. Adapt
`normalise_entry()` to your input format, then:

```python
from tools.ingest_skeleton import normalise_entry, merge_into_library
entries = [normalise_entry(r, source_name="my_team", default_license="MIT") for r in my_data]
merge_into_library(entries)
```

Re-run `python tools/search_cli.py --index` to update the index.

---

## Use with an AI agent

Best paired with **[NeXra Agent CLI](https://github.com/<owner>/nexra-cli)** —
the agent picks reference prompts from this library, calls a text-to-image
model, handles billing, and ships the result to your channels:

```bash
nexra prompt search "电商海报 中国风" --generate --model qwen
```

You can absolutely fork this repo and wire it into any agent runtime
(Claude Code, Cursor, your own). The retrieval API is just `find_similar()`.

## What's in the NeXra platform but not here

This repo ships the **license-clean** subset. The full NeXra platform also
includes:

- **1664+ prompts** (full library, including no-license entries displayed
  under fair use + attribution)
- **One-click image generation** with billing handled (5+ models)
- **14+ marketing integrations** (Meta Ads / WhatsApp / Stripe / Shopee / ...)
- **Vertical packs** for F&B, retail, property, e-commerce

If that sounds useful, see [nexra-ai.co](https://nexra-ai.co). If not, fork
freely and build your own thing — that's the point of open source.

## Roadmap

- [ ] Embedding model swap: smaller / faster options (bge-m3, jina-v3)
- [ ] Static HTML gallery generator (browse without cloning)
- [ ] Web embedding playground
- [ ] Prompt quality scoring rubric documentation
- [ ] More verticals (food photography, fashion catalogue, real estate)

## Contributing

Open an issue for:
- **Takedown requests** (if you're the original prompt author)
- **New source proposals** (bring evidence of clear license)
- **Quality issues** (mis-scored, mis-categorized, broken images)

PRs welcome for code (`tools/`, `scripts/`).

## Credits

Special thanks to the curators whose collections this builds on:
[freestylefly](https://github.com/freestylefly/awesome-gpt-image-2),
[EvoLinkAI](https://github.com/EvoLinkAI),
[jamez-bondos](https://github.com/jamez-bondos/awesome-gpt4o-images),
and 200+ original prompt authors on X.com. See [ATTRIBUTION.md](ATTRIBUTION.md)
for the full list.
