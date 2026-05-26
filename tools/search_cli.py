"""
Simple CLI for searching the prompt library.

Examples:
    python tools/search_cli.py "商务女性介绍产品"
    python tools/search_cli.py "cyberpunk city at night" --k 5 --min-score 8
    python tools/search_cli.py --index   # one-time RAG index build
"""
from __future__ import annotations

import argparse
import json
import sys

from prompt_rag import find_similar, index_all, is_ready


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", help="natural-language search query")
    ap.add_argument("--k", type=int, default=3, help="top-K results (default 3)")
    ap.add_argument("--min-score", type=int, default=7, help="minimum quality score (default 7)")
    ap.add_argument("--json", action="store_true", help="output raw JSON")
    ap.add_argument("--index", action="store_true", help="(re)build the RAG index")
    args = ap.parse_args()

    if args.index:
        print(json.dumps(index_all(verbose=True), indent=2))
        return

    if not args.query:
        ap.print_help()
        sys.exit(1)

    if not is_ready():
        print("Index not built yet. Run: python tools/search_cli.py --index", file=sys.stderr)
        sys.exit(1)

    hits = find_similar(args.query, k=args.k, min_score=args.min_score)

    if args.json:
        print(json.dumps(hits, ensure_ascii=False, indent=2))
        return

    print(f"\n  Query: {args.query}")
    print(f"  Found {len(hits)} reference prompts\n")
    for i, h in enumerate(hits, 1):
        print(f"{i}. [{h.get('score')}/10] {h.get('title')}  (similarity {h['similarity']:.3f})")
        print(f"   by {h.get('author', '?')} | {h.get('license', '?')}")
        if h.get("source_url"):
            print(f"   source: {h['source_url']}")
        print(f"   {h['prompt'][:200]}...\n")


if __name__ == "__main__":
    main()
