from __future__ import annotations

import argparse
import logging

from . import download, parse, embed_and_index, search

log = logging.getLogger("pipeline")


def main():
    parser = argparse.ArgumentParser(description="KAP RAG Pipeline")
    parser.add_argument(
        "--steps",
        nargs="+",
        choices=["download", "parse", "embed", "search", "all"],
        default=["all"],
        help="Çalıştırılacak adımlar",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="şirketin son finansal performansı ve karlılığı",
        help="search adımı için test sorgusu",
    )
    parser.add_argument(
        "--tickers",
        nargs="+",
        default=None,
        help="Sadece bu tickerlar için çalıştır (boşsa BIST 30 hepsi)",
    )
    args = parser.parse_args()

    steps = set(args.steps)
    if "all" in steps:
        steps = {"download", "parse", "embed", "search"}

    if "download" in steps:
        log.info(">>> ADIM 1: İNDİRME")
        download.run(tickers=args.tickers)

    if "parse" in steps:
        log.info(">>> ADIM 2: PARSE + CHUNK")
        parse.run()

    if "embed" in steps:
        log.info(">>> ADIM 3: EMBED + QDRANT")
        embed_and_index.index_chunks()

    if "search" in steps:
        log.info(">>> ADIM 4: TEST SORGUSU")
        print(f"\nSorgu: {args.query}")
        results = search.semantic_search(args.query, top_k=5)
        search.pretty_print(results)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    main()
