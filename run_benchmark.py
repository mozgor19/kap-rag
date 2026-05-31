"""
KAP-RAG Benchmark Sorgulama Scripti — v4
-----------------------------------------
Her soruyu RAG sistemine gönderir, top-k chunk'ları toplar ve
hem JSON hem Markdown hem CSV rapor üretir.

ÖNEMLI: Bu sistem yalnızca vektör retrieval yapar; LLM generation adımı yoktur.
"rag_answer" sütunu top-1 retrieved chunk metnini içerir; gold_answer ile
birebir karşılaştırmak için insan değerlendirmesi veya ayrı bir LLM-as-judge
katmanı gereklidir.

Kullanım:
    python run_benchmark.py                               # kap_benchmark_selected20.json, top-k=5
    python run_benchmark.py --input kap_benchmark_all.json --top-k 10
    python run_benchmark.py --no-ticker-filter            # ticker filtresi olmadan sorgula
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import re
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


def extract_kap_ids(text: str) -> set[str]:
    """KAP bildirim numaralarını metinden çıkar (KAP #, KAP ODA #, Bildirim/ formatları)."""
    return set(re.findall(r'(?:KAP(?:\s+ODA)?\s+#|Bildirim/)(\d+)', text))


def run_benchmark(bench: dict, top_k: int, use_ticker_filter: bool = True) -> list[dict]:
    from src.search import semantic_search

    questions = bench["questions"]
    results = []

    log.info("Toplam %d soru sorgulanacak (top_k=%d, ticker_filter=%s)",
             len(questions), top_k, use_ticker_filter)

    for i, q in enumerate(questions, 1):
        qid = q["id"]
        query = q["question"]
        ticker = q.get("ticker") if use_ticker_filter else None
        log.info("[%d/%d] %s — %s", i, len(questions), qid, query[:60])

        t0 = time.perf_counter()
        hits = semantic_search(query, top_k=top_k, ticker=ticker)
        elapsed = time.perf_counter() - t0

        gold_ids = extract_kap_ids(q.get("gold_answer", "")) | extract_kap_ids(q.get("document", ""))
        hit_ids: set[str] = set()
        for h in hits:
            hit_ids.update(extract_kap_ids(h.get("url", "")))

        kap_match = bool(gold_ids & hit_ids)
        top1 = hits[0] if hits else {}

        results.append({
            "id": qid,
            "ticker": q.get("ticker"),
            "category": q.get("category"),
            "difficulty": q.get("difficulty"),
            "period": q.get("period"),
            "question": query,
            "gold_answer": q.get("gold_answer", ""),
            "document": q.get("document", ""),
            "reasoning_type": q.get("reasoning_type", []),
            "human_validation_required": q.get("human_validation_required", False),
            "rag_answer": top1.get("text", "")[:600],
            "top1_score": round(float(top1.get("score", 0)), 4) if top1 else None,
            "retrieved_sources": [h.get("url", "") for h in hits],
            "gold_kap_ids": sorted(gold_ids),
            "hit_kap_ids": sorted(hit_ids),
            "kap_match": kap_match,
            "elapsed_sec": round(elapsed, 3),
            "hits": hits,
        })

    return results


def write_json(results: list[dict], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    log.info("JSON kaydedildi: %s", out_path)


def write_csv(results: list[dict], out_path: Path) -> None:
    if not results:
        return
    fieldnames = [
        "id", "category", "difficulty", "ticker", "period",
        "question", "gold_answer", "rag_answer",
        "retrieved_sources", "gold_kap_ids", "hit_kap_ids",
        "kap_match", "top1_score", "human_validation_required", "elapsed_sec",
    ]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            row = {**r}
            row["retrieved_sources"] = " | ".join(r.get("retrieved_sources", []))
            row["gold_kap_ids"] = ",".join(r.get("gold_kap_ids", []))
            row["hit_kap_ids"] = ",".join(r.get("hit_kap_ids", []))
            writer.writerow(row)
    log.info("CSV kaydedildi: %s", out_path)


def write_markdown(results: list[dict], meta: dict, out_path: Path) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    recall = sum(1 for r in results if r["kap_match"])
    n = len(results)

    lines: list[str] = [
        f"# KAP-RAG Benchmark — RAG Sonuçları",
        f"",
        f"**Üretildi:** {ts}  ",
        f"**Dataset:** {meta.get('dataset', '—')} v{meta.get('version', '?')}  ",
        f"**Evaluation target:** {meta.get('evaluation_target', '—')}  ",
        f"**Soru sayısı:** {n}  ",
        f"**Corpus snapshot:** {meta.get('corpus_snapshot_date', '—')} (knowledge cutoff: {meta.get('knowledge_cutoff', '—')})  ",
        f"",
        f"## Özet Skor Tablosu",
        f"",
        f"| Metrik | Değer |",
        f"|--------|-------|",
        f"| KAP belgesi recall@k | **{recall}/{n} ({100*recall//n}%)** |",
        f"| Ortalama top-1 cosine skor | {sum(r['top1_score'] or 0 for r in results)/n:.4f} |",
        f"| Median sorgu süresi | {sorted(r['elapsed_sec'] for r in results)[n//2]:.3f}s |",
        f"",
        f"### Kategori Bazlı Recall",
        f"",
        f"| Kategori | Recall@k | N |",
        f"|----------|----------|---|",
    ]

    cats: dict[str, list] = {}
    for r in results:
        cats.setdefault(r["category"], []).append(r["kap_match"])
    for cat, matches in sorted(cats.items()):
        h = sum(matches)
        lines.append(f"| {cat} | {h}/{len(matches)} | {len(matches)} |")

    lines += [
        f"",
        f"> **Not:** Bu recall metriği gold KAP bildirim numarasının top-{results[0]['hits'].__len__() if results else '?'} sonuçlarında görünüp görünmediğini ölçer.",
        f"> `rag_answer` sütunu LLM üretimi değil, top-1 retrieved chunk'ın ilk 600 karakteridir.",
        f"",
        "---",
        "",
    ]

    for r in results:
        match_icon = "✓" if r["kap_match"] else "✗"
        lines += [
            f"## {match_icon} {r['id']} · {r['ticker']} · {r['category']} · {r['difficulty']}",
            f"",
            f"**Dönem:** {r['period']}  ",
            f"**Kaynak belge:** {r['document']}  ",
            f"**Top-1 skor:** {r['top1_score']}  |  **KAP match:** {match_icon}  |  **Süre:** {r['elapsed_sec']}s  ",
            f"**human_validation_required:** {r['human_validation_required']}  ",
            f"",
            f"### Soru",
            f"> {r['question']}",
            f"",
            f"### Gold Answer",
            f"> {r['gold_answer']}",
            f"",
            f"### RAG Top-1 Retrieved Chunk  _(retrieval only — LLM generation yok)_",
            f"",
            f"```",
            (r["rag_answer"] or "—").replace("```", "'''"),
            f"```",
            f"",
            f"**Retrieved sources (top-{len(r['retrieved_sources'])}):**",
        ]

        for j, (url, h) in enumerate(zip(r["retrieved_sources"], r["hits"]), 1):
            lines.append(
                f"- [{j}] skor=`{h['score']:.4f}` — {url} — {(h.get('subject') or '—')[:60]}"
            )

        gold_str = ",".join(r["gold_kap_ids"]) or "—"
        hit_str = ",".join(r["hit_kap_ids"]) or "—"
        lines += [
            f"",
            f"**Gold KAP#:** {gold_str} | **Hit KAP#:** {hit_str}",
            f"",
            "---",
            "",
        ]

    out_path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Markdown kaydedildi: %s", out_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="KAP-RAG Benchmark Sorgulama v4")
    parser.add_argument(
        "--input", type=Path, default=Path("kap_benchmark_selected20.json"),
        help="Benchmark JSON dosyası",
    )
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument(
        "--out-dir", type=Path, default=Path("."),
        help="Çıktı dizini",
    )
    parser.add_argument(
        "--no-ticker-filter", action="store_true",
        help="Qdrant'ta ticker filtresi kullanma",
    )
    args = parser.parse_args()

    if not args.input.exists():
        log.error("Benchmark dosyası bulunamadı: %s", args.input)
        sys.exit(1)

    bench = load_benchmark(args.input)
    meta = bench.get("metadata", {})

    results = run_benchmark(bench, top_k=args.top_k, use_ticker_filter=not args.no_ticker_filter)

    ts_file = datetime.now().strftime("%Y%m%d_%H%M")
    stem = args.input.stem
    json_out = args.out_dir / f"benchmark_results_{stem}_{ts_file}.json"
    md_out   = args.out_dir / f"benchmark_results_{stem}_{ts_file}.md"
    csv_out  = args.out_dir / f"benchmark_results_{stem}_{ts_file}.csv"

    write_json(results, json_out)
    write_csv(results, csv_out)
    write_markdown(results, meta, md_out)

    recall = sum(1 for r in results if r["kap_match"])
    log.info("Tamamlandı. Recall@%d: %d/%d (%%%.0f)",
             args.top_k, recall, len(results), 100*recall/len(results) if results else 0)
    log.info("Çıktılar: %s | %s | %s", json_out.name, csv_out.name, md_out.name)


if __name__ == "__main__":
    main()
