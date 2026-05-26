# Attribution & Per-Source Licensing

This repository aggregates AI image prompts from multiple open sources. The
**code** in this repo is Apache 2.0 (see [LICENSE](LICENSE)). The **prompt data**
in `data/prompts.json` carries per-entry license metadata in the `license` field.

## Source Breakdown (955 entries)

| Source | Count | License (per-entry `license` field) | Notes |
|---|---:|---|---|
| `awesome-gpt-image-2` | 402 | `Attribution Required (X.com public post)` | Originally aggregated by [@freestylefly](https://github.com/freestylefly/awesome-gpt-image-2). Underlying prompts are X.com public posts by 237 unique authors. |
| `evolink` | 343 | `Apache 2.0` | From [EvoLinkAI](https://github.com/EvoLinkAI) prompt repositories. |
| `youmind` | 127 | `CC BY 4.0` | From [youmind.com](https://youmind.com); per their ToS, users retain ownership and have full commercial-use rights. |
| `vision_ai` | 48 | `CC BY 4.0` | Originally authored by the NeXra team. |
| `jamez-bondos-gpt1` | 35 | `OpenAI Example` | OpenAI [gpt-image-1 cookbook examples](https://github.com/jamez-bondos/awesome-gpt4o-images) by [@jamez-bondos](https://github.com/jamez-bondos). |

## How to Use

- **Every entry** carries `author`, `source`, `source_url`, and `license` fields.
- If you redistribute, mirror, or build a product on top of any prompt, **preserve these fields** — that's the attribution chain.
- For `Attribution Required (X.com public post)`, treat the prompt as fair-use aggregation: cite the original X author + link to their post.
- For `Apache 2.0`, retain the [NOTICE](NOTICE) file and state any modifications.
- For `CC BY 4.0`, credit the author + link to source.
- For `OpenAI Example`, credit OpenAI's cookbook.

## Removal Requests

If you are an original author and want your prompt removed, open an issue with
the `source_url` of the entry. We'll honor takedowns within 7 days.

## Not Included In This Repo

3 source buckets (~656 entries) in our internal library are not redistributed
here because they carry no clear license (= All Rights Reserved by default):

- `peterRooo` — [peterRooo/awesome-gpt-image-2-prompts](https://github.com/peterRooo/awesome-gpt-image-2-prompts) (No LICENSE file)
- `0aicoder0` — [0aicoder0/Ultimate-ChatGPT-Image-and-Nano-Banana-Pro-Collection](https://github.com/0aicoder0/Ultimate-ChatGPT-Image-and-Nano-Banana-Pro-Collection) (No LICENSE file)
- `facebook_group` — anonymous FB-group submissions

These remain in the private NeXra platform under fair-use display + attribution,
but are not part of this open-source release.
