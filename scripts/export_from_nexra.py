"""
Export license-clean subset from NeXra prompts.json → public repo data.

Whitelist sources (license verified):
  - evolink (EvoLinkAI GitHub org, Apache 2.0)
  - vision_ai (NeXra in-house)
  - jamez-bondos-gpt1 (OpenAI cookbook examples)
  - awgi2 / awesome-gpt-image-2 (X.com attribution, same footing as freestylefly)
  - youmind (CC BY 4.0 via youmind ToS)

Excluded (no license):
  - peterRooo, 0aicoder0, facebook_group (No License = All Rights Reserved)
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

SRC_JSON = Path("/Users/j.voguemacmini/.openclaw/nexra-storefront/apps/nexra-platform/public/data/prompts.json")
SRC_IMG = Path("/Users/j.voguemacmini/.openclaw/nexra-storefront/apps/nexra-platform/public/images/prompts")
DST_REPO = Path("/Users/j.voguemacmini/.openclaw/workspace/awesome-ai-image-prompts")
DST_JSON = DST_REPO / "data" / "prompts.json"
DST_IMG = DST_REPO / "data" / "images"

WHITELIST = {"evolink", "vision_ai", "jamez-bondos-gpt1", "awesome-gpt-image-2", "youmind"}
# Public-safe fields only; drop SEO internals, quality_reasons, image_local etc.
PUBLIC_FIELDS = [
    "id", "title", "title_en", "title_zh", "title_ms",
    "prompt", "prompt_zh", "prompt_ms",
    "category", "category_label", "category_raw",
    "image_url", "has_image",
    "source", "source_url", "author", "author_url",
    "license", "lang",
    "quality_score",
    "seo_keywords",
    "styles_raw", "scenes_raw",
]


def main():
    DST_IMG.mkdir(parents=True, exist_ok=True)
    all_entries = json.load(open(SRC_JSON))

    selected = []
    images_copied = 0
    images_missing = 0
    by_source = {}
    by_license = {}

    for p in all_entries:
        src = p.get("source", "")
        if src not in WHITELIST:
            continue
        if not p.get("visible", True):
            continue
        if not p.get("prompt", "").strip():
            continue

        entry = {k: p.get(k) for k in PUBLIC_FIELDS if k in p}

        img_url = entry.get("image_url") or ""
        if img_url.startswith("/images/prompts/"):
            fn = img_url.rsplit("/", 1)[-1]
            src_img = SRC_IMG / fn
            if src_img.exists():
                shutil.copy2(src_img, DST_IMG / fn)
                entry["image_url"] = f"data/images/{fn}"
                images_copied += 1
            else:
                entry["image_url"] = ""
                entry["has_image"] = False
                images_missing += 1

        selected.append(entry)
        by_source[src] = by_source.get(src, 0) + 1
        lic = entry.get("license", "Unknown")
        by_license[lic] = by_license.get(lic, 0) + 1

    DST_JSON.write_text(json.dumps(selected, ensure_ascii=False, indent=2), "utf-8")

    print(f"Exported {len(selected)} entries to {DST_JSON.relative_to(DST_REPO)}")
    print(f"Images copied: {images_copied} (missing: {images_missing})")
    print("\nBy source:")
    for s, n in sorted(by_source.items(), key=lambda x: -x[1]):
        print(f"  {s}: {n}")
    print("\nBy license:")
    for l, n in sorted(by_license.items(), key=lambda x: -x[1]):
        print(f"  {l}: {n}")


if __name__ == "__main__":
    main()
