"""
RAG retrieval for the awesome-ai-image-prompts library.

Self-contained: Qdrant local persistence + fastembed multilingual-e5-large.
First run downloads ~1.5GB embedding model to ~/.cache/fastembed.

Usage:
    from tools.prompt_rag import index_all, find_similar
    index_all()  # one-time, embeds data/prompts.json into local Qdrant
    hits = find_similar("商务女性介绍产品", k=3)
"""
from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).parent.parent
PROMPTS_JSON = REPO_ROOT / "data" / "prompts.json"
QDRANT_PATH = REPO_ROOT / ".qdrant"
COLLECTION = "ai_image_prompts_v1"
EMBED_DIM = 1024
EMBED_MODEL_NAME = "intfloat/multilingual-e5-large"
QUALITY_THRESHOLD = 6


_fastembed_model = None
_qdrant_client = None


def _embedder():
    global _fastembed_model
    if _fastembed_model is None:
        from fastembed import TextEmbedding
        logger.info("Loading %s (first run downloads ~1.5GB)", EMBED_MODEL_NAME)
        _fastembed_model = TextEmbedding(model_name=EMBED_MODEL_NAME)
    return _fastembed_model


def _qdrant():
    global _qdrant_client
    if _qdrant_client is None:
        from qdrant_client import QdrantClient
        QDRANT_PATH.mkdir(parents=True, exist_ok=True)
        _qdrant_client = QdrantClient(path=str(QDRANT_PATH))
    return _qdrant_client


def embed_texts(texts: list[str], is_query: bool = False) -> list[list[float]]:
    if not texts:
        return []
    prefix = "query: " if is_query else "passage: "
    prefixed = [prefix + t for t in texts]
    return [v.tolist() for v in _embedder().embed(prefixed)]


def _stable_int_id(s: str) -> int:
    h = hashlib.md5(s.encode("utf-8")).digest()
    return int.from_bytes(h[:8], "big") & 0x7FFFFFFFFFFFFFFF


def _embed_text(p: dict) -> str:
    title = (p.get("title_en") or p.get("title") or "").strip()
    body = (p.get("prompt") or "").strip()
    return f"{title}\n\n{body}"[:7500]


def ensure_collection() -> None:
    from qdrant_client.models import Distance, VectorParams
    cli = _qdrant()
    existing = {c.name for c in cli.get_collections().collections}
    if COLLECTION not in existing:
        cli.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
        )


def index_all(verbose: bool = True, batch: int = 32) -> dict:
    from qdrant_client.models import PointStruct
    ensure_collection()
    cli = _qdrant()
    data = json.loads(PROMPTS_JSON.read_text("utf-8"))
    eligible = [p for p in data if (p.get("quality_score") or 0) >= QUALITY_THRESHOLD and p.get("prompt")]
    if verbose:
        print(f"Indexing {len(eligible)} of {len(data)} prompts (score >= {QUALITY_THRESHOLD})")

    indexed = 0
    for i in range(0, len(eligible), batch):
        chunk = eligible[i:i + batch]
        vectors = embed_texts([_embed_text(p) for p in chunk])
        points = [
            PointStruct(
                id=_stable_int_id(p["id"]),
                vector=v,
                payload={
                    "id": p["id"],
                    "title": p.get("title_en") or p.get("title", ""),
                    "title_zh": p.get("title_zh"),
                    "category": p.get("category"),
                    "image_url": p.get("image_url"),
                    "score": p.get("quality_score"),
                    "author": p.get("author"),
                    "source": p.get("source"),
                    "source_url": p.get("source_url"),
                    "license": p.get("license"),
                    "prompt": p.get("prompt", "")[:2000],
                },
            ) for p, v in zip(chunk, vectors)
        ]
        cli.upsert(collection_name=COLLECTION, points=points)
        indexed += len(points)
        if verbose and (i // batch) % 5 == 0:
            print(f"  [{i+len(chunk)}/{len(eligible)}]")

    return {"indexed": indexed, "total_eligible": len(eligible), "total": len(data)}


def find_similar(query: str, k: int = 5, min_score: int = 7) -> list[dict]:
    if not query.strip():
        return []
    ensure_collection()
    vectors = embed_texts([query], is_query=True)
    if not vectors:
        return []
    from qdrant_client.models import Filter, FieldCondition, Range
    results = _qdrant().query_points(
        collection_name=COLLECTION,
        query=vectors[0],
        limit=k * 2,
        query_filter=Filter(must=[FieldCondition(key="score", range=Range(gte=min_score))]),
    )
    return [{**(p.payload or {}), "similarity": float(p.score)} for p in results.points[:k]]


def is_ready() -> bool:
    try:
        ensure_collection()
        return _qdrant().get_collection(COLLECTION).points_count > 0
    except Exception:
        return False
