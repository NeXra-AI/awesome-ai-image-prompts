# Using awesome-ai-image-prompts with an AI Agent

This library is designed to be **retrieved by an agent** before it writes a
final prompt for a t2i / i2i model. Three integration patterns below.

## Pattern 1 — Few-shot examples for prompt expansion

When a user describes an image in 5–15 words and you want to expand it into
a production-grade prompt, retrieve 3 high-quality references first and feed
them to your LLM as few-shot examples.

```python
from tools.prompt_rag import find_similar

def enhance_prompt(short_desc: str) -> str:
    hits = find_similar(short_desc, k=3, min_score=8)
    few_shot = "\n\n".join(
        f"Example {i+1} (by {h['author']}):\n{h['prompt']}"
        for i, h in enumerate(hits)
    )
    system = f"""You are a t2i prompt engineer. Use these reference examples
to match density and style — do NOT copy verbatim.

{few_shot}

User wants: {short_desc}
Write a detailed prompt now."""
    return call_your_llm(system)
```

## Pattern 2 — Agent tool / function call

Register `find_similar` as a tool your agent can call. Anthropic schema:

```python
{
  "name": "search_prompt_examples",
  "description": "Search the prompt library for high-quality image/video prompt references. Returns title, prompt body, quality score, category, original author/source URL. Use to ground prompt-writing in real examples; cite source when answering.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "k": {"type": "integer", "default": 3},
      "min_score": {"type": "integer", "default": 7}
    },
    "required": ["query"]
  }
}
```

Handler:

```python
async def handle_search_prompt_examples(query: str, k: int = 3, min_score: int = 7):
    from tools.prompt_rag import find_similar
    hits = find_similar(query, k=k, min_score=min_score)
    return {"ok": True, "count": len(hits), "examples": hits}
```

## Pattern 3 — NeXra Agent CLI (no glue code)

If you don't want to wire anything yourself:

```bash
nexra prompt search "电商海报 中国风" --k 3
nexra prompt generate --from-search "cyberpunk product shot" --model qwen
```

See [NeXra Agent CLI](https://github.com/<owner>/nexra-cli).

## Attribution rule

Whichever pattern you use, when your agent surfaces a prompt to the end user,
**show the original author + source URL**. Every entry in `data/prompts.json`
has `author`, `source_url`, and `license` fields — they're not optional metadata.
