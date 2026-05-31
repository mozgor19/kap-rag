"""
KAP-RAG Benchmark Sorgulama Scripti
------------------------------------
Her soruyu RAG sistemine gönderir, top-k sonuçları toplar ve
hem JSON hem de okunabilir Markdown rapor üretir.

Kullanım:
    python run_benchmark.py                          # kap_rag_benchmark_cleaned.json
    python run_benchmark.py --input my_bench.json   # başka dosya
    python run_benchmark.py --top-k 10              # daha fazla sonuç
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("benchmark")


def load_benchmark(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def run_benchmark(bench: dict, top_k: int) -> list[dict]:
    from src.search import semantic_search

    questions = bench["questions"]
    results = []

    log.info("Toplam %d soru sorgulanacak (top_k=%d)", len(questions), top_k)

    for i, q in enumerate(questions, 1):
        qid = q["id"]
        query = q["question"]
        log.info("[%d/%d] %s — %s", i, len(questions), qid, query[:60])

        t0 = time.perf_counter()
        hits = semantic_search(
            query,
            top_k=top_k,
            ticker=q.get("ticker"),
        )
        elapsed = time.perf_counter() - t0

        results.append({
            "id": qid,
            "ticker": q.get("ticker"),
            "category": q.get("category"),
            "difficulty": q.get("difficulty"),
            "period": q.get("period"),
            "question": query,
            "gold_answer": q.get("gold_answer", ""),
            "document": q.get("document", ""),
            "elapsed_sec": round(elapsed, 3),
            "hits": hits,
        })

    return results


def write_json(results: list[dict], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    log.info("JSON kaydedildi: %s", out_path)


def write_markdown(results: list[dict], meta: dict, out_path: Path) -> None:
    lines: list[str] = []

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines += [
        f"# KAP-RAG Benchmark — RAG Sonuçları",
        f"",
        f"**Üretildi:** {ts}  ",
        f"**Dataset:** {meta.get('dataset', '—')}  ",
        f"**Soru sayısı:** {len(results)}  ",
        f"",
        "---",
        "",
    ]

    for r in results:
        lines += [
            f"## {r['id']} · {r['ticker']} · {r['category']} · {r['difficulty']}",
            f"",
            f"**Dönem:** {r['period']}  ",
            f"**Kaynak belge:** {r['document']}  ",
            f"",
            f"### Soru",
            f"",
            f"> {r['question']}",
            f"",
            f"### Gold Answer",
            f"",
            f"> {r['gold_answer']}",
            f"",
            f"### RAG Sonuçları  _(sorgu süresi: {r['elapsed_sec']}s)_",
            f"",
        ]

        if not r["hits"]:
            lines.append("_Sonuç bulunamadı._\n")
        else:
            for j, h in enumerate(r["hits"], 1):
                snippet = h["text"][:400].replace("\n", " ")
                if len(h["text"]) > 400:
                    snippet += "…"
                lines += [
                    f"**[{j}]** skor=`{h['score']:.4f}` · {h['ticker']} · {h['subject'] or '—'}  ",
                    f"📅 {h['publish_datetime']}  ",
                    f"🔗 {h['url']}  ",
                    f"",
                    f"```",
                    snippet,
                    f"```",
                    f"",
                ]

        lines.append("---\n")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Markdown kaydedildi: %s", out_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="KAP-RAG Benchmark Sorgulama")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("kap_rag_benchmark_cleaned.json"),
        help="Benchmark JSON dosyası",
    )
    parser.add_argument("--top-k", type=int, default=5, help="Her soru için döndürülecek sonuç sayısı")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("."),
        help="Çıktı dizini",
    )
    args = parser.parse_args()

    bench_path = args.input
    if not bench_path.exists():
        log.error("Benchmark dosyası bulunamadı: %s", bench_path)
        sys.exit(1)

    bench = load_benchmark(bench_path)
    meta = bench.get("metadata", {})

    results = run_benchmark(bench, top_k=args.top_k)

    ts_file = datetime.now().strftime("%Y%m%d_%H%M")
    json_out = args.out_dir / f"benchmark_results_{ts_file}.json"
    md_out = args.out_dir / f"benchmark_results_{ts_file}.md"

    write_json(results, json_out)
    write_markdown(results, meta, md_out)

    log.info("Tamamlandı. Toplam %d soru.", len(results))


if __name__ == "__main__":
    main()
