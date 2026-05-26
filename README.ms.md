# awesome-ai-image-prompts

**🌍 [English](README.md) · [简体中文](README.zh-CN.md) · [Bahasa Melayu](README.ms.md)**

> **Pustaka Prompt-as-Code** — 955 prompt terkurasi untuk GPT-Image-2,
> Nano Banana, Seedance, Qwen-VL, Gemini Imagen dan lain-lain.
> Apache 2.0. Berbilang bahasa (zh / en / ms). **RAG sedia guna.**

[![License](https://img.shields.io/badge/code-Apache%202.0-blue.svg)](LICENSE)
[![Prompts](https://img.shields.io/badge/prompts-955-green.svg)](data/prompts.json)
[![Languages](https://img.shields.io/badge/languages-zh%20%7C%20en%20%7C%20ms-orange.svg)](#berbilang-bahasa)

---

## Apa ini

Sebuah pustaka prompt **boleh dicari** untuk penjanaan imej AI, disaring
daripada sumber awam dengan **atribusi dan metadata lesen setiap entri**.
Tidak seperti senarai prompt "awesome-*" biasa, repo ini menyediakan:

- **955 prompt** dalam skema JSON berstruktur (bukan markdown gallery)
- **Skor kualiti setiap entri** (1–10), boleh ditapis ikut tier semasa carian
- **Metadata berbilang bahasa** (zh / en / ms)
- **Pipeline RAG lengkap** (Qdrant + e5 embedding) — clone, jalan dalam 5 minit
- **Skaffolding BYOP** untuk menambah prompt anda sendiri

Repo ini **agnostik model**. Prompt berfungsi dengan GPT-Image-2 (sasaran asal),
Google Nano Banana, Seedance, Qwen-VL, Gemini Imagen, dan mana-mana model
text-to-image yang kuat.

## Kenapa satu lagi repo prompt?

Kebanyakan senarai "awesome-*" prompt adalah pamer markdown — cantik dilihat,
sukar diintegrasikan. Yang ini direka untuk **dipanggil oleh agent**:

```python
from tools.prompt_rag import find_similar
hits = find_similar("商务女性介绍产品", k=3)
# → [{'title': '...', 'score': 8, 'prompt': '...', 'author': '@...'}, ...]
```

Masukkan `hits` terus ke dalam system prompt Qwen / GPT / Claude anda sebagai
contoh few-shot, dan kualiti imej meningkat ketara.

## Mula cepat

```bash
git clone https://github.com/NeXra-AI/awesome-ai-image-prompts.git
cd awesome-ai-image-prompts
pip install -r tools/requirements.txt

# Sekali sahaja: bina indeks Qdrant tempatan (run pertama muat turun ~1.5GB model e5)
python tools/search_cli.py --index

# Kemudian cari:
python tools/search_cli.py "cyberpunk product shot, neon, night"
python tools/search_cli.py "poster e-commerce gaya Cina merah" --k 5 --min-score 8
```

Output:

```
  Query: poster e-commerce gaya Cina merah
  Found 3 reference prompts

1. [8/10] 红蓝光影下的未来都市双重曝光青年  (similarity 0.872)
   by Fujimoto_hina | Attribution Required (X.com public post)
   source: https://x.com/Fujimoto_hina/status/...
   一位年轻男子的超写实电影级双重曝光侧脸肖像...
```

## Struktur repo

```
awesome-ai-image-prompts/
├── data/
│   ├── prompts.json     # 955 entri, skema berstruktur
│   └── images/          # 953 imej rujukan
├── tools/
│   ├── prompt_rag.py    # Pipeline RAG Qdrant + e5
│   ├── search_cli.py    # Carian satu-baris
│   ├── ingest_skeleton.py  # Skaffolding BYOP
│   └── requirements.txt
├── scripts/
│   └── export_from_nexra.py  # Cara korpus ini dipasang
├── LICENSE              # Apache 2.0 (kod)
├── NOTICE               # Atribusi diwajibkan
└── ATTRIBUTION.md       # Pecahan lesen ikut sumber
```

## Skema data

Setiap entri dalam `data/prompts.json`:

```jsonc
{
  "id": "awgi2-469",
  "title": "导览式科普绘本",
  "title_en": "...", "title_zh": "...", "title_ms": "...",
  "prompt": "...",
  "category": "illustration",
  "source": "awesome-gpt-image-2",
  "source_url": "https://x.com/MrLarus/status/...",
  "author": "MrLarus",
  "license": "Attribution Required (X.com public post)",
  "lang": "zh",
  "quality_score": 8,
  "seo_keywords": { "en": [...], "zh": [...], "ms": [...] }
}
```

## Lesen & atribusi

- **Kod** dalam `tools/` dan `scripts/`: Apache 2.0 (LICENSE + NOTICE)
- **Prompt** dalam `data/prompts.json`: lesen setiap entri di medan `license`

Lihat **[ATTRIBUTION.md](ATTRIBUTION.md)** untuk pecahan penuh ikut sumber.
**Sentiasa kekalkan `author`, `source`, `source_url`, `license`** apabila
mengedar semula.

## Berbilang bahasa

Semua entri membawa `title_en` / `title_zh` / `title_ms` dan `prompt_zh` /
`prompt_ms` di mana tersedia. Berguna untuk:

- Cadangan prompt setempat dalam UI anda
- Carian ikut bahasa pilihan pengguna
- Pertanyaan RAG silang bahasa (model e5 menangani padanan silang bahasa)

## Bring Your Own Prompts (BYOP)

`tools/ingest_skeleton.py` menunjukkan skema dan corak deduplikasi. Sesuaikan
`normalise_entry()` ke format input anda, kemudian:

```python
from tools.ingest_skeleton import normalise_entry, merge_into_library
entries = [normalise_entry(r, source_name="my_team", default_license="MIT") for r in my_data]
merge_into_library(entries)
```

Jalankan semula `python tools/search_cli.py --index` untuk kemas kini indeks.

---

## Guna dengan AI Agent

Pasangan terbaik: **[NeXra Agent CLI](https://github.com/NeXra-AI/agent-cli)** —
agent memilih prompt rujukan dari pustaka ini, panggil model text-to-image,
uruskan caj, dan hantar hasil ke saluran anda:

```bash
nexra prompt search "poster e-commerce gaya Cina" --generate --model qwen
```

Anda boleh fork repo ini dan wayar ke mana-mana agent runtime (Claude Code,
Cursor, sendiri). API carian hanyalah `find_similar()`.

## Apa yang ada di NeXra tapi tiada di sini

Repo ini ship subset **bersih-lesen**. Platform NeXra penuh juga termasuk:

- **1664+ prompt** (pustaka penuh, termasuk entri tanpa lesen yang dipaparkan
  bawah fair use + atribusi)
- **Penjanaan imej satu klik** dengan caj diuruskan (5+ model)
- **14+ integrasi pemasaran** (Meta Ads / WhatsApp / Stripe / Shopee / ...)
- **Pek vertikal** untuk F&B, runcit, hartanah, e-dagang

Lihat [nexra-ai.co](https://nexra-ai.co). Tidak perlu? Fork bebas dan bina
sendiri — itu tujuan open source.

## Peta jalan

- [ ] Tukar model embedding: pilihan lebih kecil/laju (bge-m3, jina-v3)
- [ ] Penjana galeri HTML statik (lihat tanpa clone)
- [ ] Web embedding playground
- [ ] Dokumentasi rubrik skor kualiti prompt
- [ ] Lebih vertikal (fotografi makanan, katalog fesyen, hartanah)

## Sumbangan

Buka isu untuk:
- **Permintaan penyingkiran** (jika anda penulis asal)
- **Cadangan sumber baru** (bawa bukti lesen yang jelas)
- **Isu kualiti** (skor salah, kategori salah, imej rosak)

PR dialu-alukan (`tools/`, `scripts/`).

## Penghargaan

Terima kasih khusus kepada kurator yang himpunan mereka asas kami:
[freestylefly](https://github.com/freestylefly/awesome-gpt-image-2),
[EvoLinkAI](https://github.com/EvoLinkAI),
[jamez-bondos](https://github.com/jamez-bondos/awesome-gpt4o-images),
dan 200+ penulis prompt asal di X.com. Senarai penuh dalam
[ATTRIBUTION.md](ATTRIBUTION.md).
