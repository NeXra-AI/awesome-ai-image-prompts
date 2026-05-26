"""
Bring Your Own Prompts (BYOP) — ingest skeleton.

Adapt this to import prompts from any source (your CSV, your scraped X archive,
your team's Notion DB) into the unified schema, then run prompt_rag.index_all()
to make them retrievable.

Required fields per entry:
  id, title, prompt, source, license

Optional but recommended:
  category, image_url, author, source_url, lang, quality_score,
  title_en/zh/ms, prompt_zh/ms, seo_keywords
"""
from __future__ import annotations

import json
from pathlib import Path

PROMPTS_JSON = Path(__file__).parent.parent / "data" / "prompts.json"


def detect_lang(text: str) -> str:
    if not text:
        return "en"
    cn = sum(1 for c in text[:500] if "一" <= c <= "鿿")
    return "zh" if cn > 20 else "en"


def normalise_entry(raw: dict, source_name: str, default_license: str) -> dict:
    """Map your input format to the unified schema. Customize this function."""
    prompt = (raw.get("prompt") or raw.get("text") or "").strip()
    title = (raw.get("title") or prompt[:60]).strip()
    lang = detect_lang(prompt)
    return {
        "id": f"{source_name}-{raw.get('id') or raw.get('uid')}",
        "title": title,
        "title_en": title if lang == "en" else "",
        "title_zh": title if lang == "zh" else "",
        "prompt": prompt,
        "prompt_zh": prompt if lang == "zh" else "",
        "category": raw.get("category") or "other",
        "image_url": raw.get("image_url") or "",
        "has_image": bool(raw.get("image_url")),
        "source": source_name,
        "source_url": raw.get("source_url") or "",
        "author": raw.get("author") or "unknown",
        "lang": lang,
        "license": default_license,
        "quality_score": int(raw.get("score") or 7),
    }


def merge_into_library(new_entries: list[dict], dedupe_field: str = "source_url"):
    """Append new entries to data/prompts.json, dedupe by `dedupe_field`."""
    existing = json.loads(PROMPTS_JSON.read_text("utf-8")) if PROMPTS_JSON.exists() else []
    seen = {e.get(dedupe_field) for e in existing if e.get(dedupe_field)}

    added = 0
    for e in new_entries:
        key = e.get(dedupe_field)
        if key and key in seen:
            continue
        existing.append(e)
        if key:
            seen.add(key)
        added += 1

    PROMPTS_JSON.write_text(json.dumps(existing, ensure_ascii=False, indent=2), "utf-8")
    print(f"Added {added} entries (skipped {len(new_entries) - added} duplicates). Total: {len(existing)}")
    print("Now run: python tools/search_cli.py --index")


if __name__ == "__main__":
    # Example: ingest a JSONL of your own prompts
    # raw_lines = [json.loads(l) for l in open("my_prompts.jsonl")]
    # entries = [normalise_entry(r, source_name="my_team", default_license="MIT") for r in raw_lines]
    # merge_into_library(entries)
    print(__doc__)
