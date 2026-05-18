from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterator

from pypdf import PdfReader

from .config import CONFIG

log = logging.getLogger("parse")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)


def extract_text_from_pdf(pdf_path: Path) -> str:
    try:
        reader = PdfReader(str(pdf_path))
        pages = []
        for page in reader.pages:
            try:
                pages.append(page.extract_text() or "")
            except Exception as e:
                log.debug("Sayfa parse hatası %s: %s", pdf_path.name, e)
        return "\n\n".join(pages)
    except Exception as e:
        log.warning("PDF açılamadı %s: %s", pdf_path.name, e)
        return ""


def clean_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"-\n(\w)", r"\1", text)
    text = re.sub(r"\n\s*\d{1,3}\s*\n", "\n", text)
    return text.strip()


def chunk_text(
    text: str,
    chunk_size: int = CONFIG.chunk_size,
    overlap: int = CONFIG.chunk_overlap,
) -> list[str]:
    if len(text) <= chunk_size:
        return [text] if len(text) >= CONFIG.min_chunk_chars else []

    chunks = []
    sentences = re.split(r"(?<=[.!?])\s+", text)

    current: list[str] = []
    current_len = 0
    for sent in sentences:
        sent_len = len(sent)
        if current_len + sent_len > chunk_size and current:
            chunk = " ".join(current).strip()
            if len(chunk) >= CONFIG.min_chunk_chars:
                chunks.append(chunk)
            overlap_chars = 0
            overlap_buf = []
            for s in reversed(current):
                if overlap_chars + len(s) > overlap:
                    break
                overlap_buf.insert(0, s)
                overlap_chars += len(s) + 1
            current = overlap_buf
            current_len = overlap_chars
        current.append(sent)
        current_len += sent_len + 1

    if current:
        chunk = " ".join(current).strip()
        if len(chunk) >= CONFIG.min_chunk_chars:
            chunks.append(chunk)

    return chunks


@dataclass
class ChunkRecord:
    chunk_id: str
    text: str
    ticker: str
    company_name: str
    disclosure_index: int
    publish_datetime: str
    subject: str
    disclosure_type: str
    is_corrective: bool
    is_late: bool
    url: str
    source_filename: str
    chunk_position: int


def iter_disclosure_chunks() -> Iterator[ChunkRecord]:
    meta_files = sorted(CONFIG.metadata_dir.glob("*.json"))
    log.info("%d şirket metadata dosyası bulundu", len(meta_files))

    for meta_file in meta_files:
        ticker = meta_file.stem
        try:
            records = json.loads(meta_file.read_text(encoding="utf-8"))
        except Exception as e:
            log.warning("Metadata okunamadı %s: %s", meta_file, e)
            continue

        for disc in records:
            for att in disc.get("attachments", []):
                pdf_path = CONFIG.project_root / att["local_path"]
                if not pdf_path.exists():
                    continue

                raw = extract_text_from_pdf(pdf_path)
                cleaned = clean_text(raw)
                if len(cleaned) < CONFIG.min_chunk_chars:
                    continue

                chunks = chunk_text(cleaned)
                for i, ch in enumerate(chunks):
                    yield ChunkRecord(
                        chunk_id=f"{disc['index']}_{pdf_path.stem}_{i}",
                        text=ch,
                        ticker=ticker,
                        company_name=disc.get("company_name", ""),
                        disclosure_index=disc["index"],
                        publish_datetime=disc["publish_datetime"],
                        subject=disc.get("subject", ""),
                        disclosure_type=disc.get("disclosure_type", ""),
                        is_corrective=disc.get("is_corrective", False),
                        is_late=disc.get("is_late", False),
                        url=disc.get("url", ""),
                        source_filename=pdf_path.name,
                        chunk_position=i,
                    )


def run() -> Path:
    out_path = CONFIG.text_dir / "chunks.jsonl"
    CONFIG.text_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    with out_path.open("w", encoding="utf-8") as f:
        for chunk in iter_disclosure_chunks():
            f.write(json.dumps(asdict(chunk), ensure_ascii=False) + "\n")
            count += 1
            if count % 100 == 0:
                log.info("  %d chunk yazıldı...", count)

    log.info("✓ Toplam %d chunk → %s", count, out_path)
    return out_path


if __name__ == "__main__":
    run()
