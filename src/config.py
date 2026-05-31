from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path


try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).resolve().parent.parent / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
except ImportError:
    pass


def _env_date(name: str, default: date) -> date:
    value = os.getenv(name)
    if not value:
        return default
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{name} geçersiz tarih: {value!r}. YYYY-MM-DD formatı bekleniyor.") from exc


@dataclass(frozen=True)
class Config:
    end_date: date = field(
        default_factory=lambda: _env_date("KAP_END_DATE", date.today())
    )
    start_date: date = field(
        default_factory=lambda: _env_date(
            "KAP_START_DATE",
            _env_date("KAP_END_DATE", date.today())
            - timedelta(days=int(os.getenv("KAP_LOOKBACK_DAYS", "90"))),
        )
    )

    def __post_init__(self) -> None:
        if self.start_date > self.end_date:
            raise ValueError(
                f"KAP_START_DATE ({self.start_date}) KAP_END_DATE ({self.end_date})'den "
                "büyük olamaz. Tarih aralığını kontrol edin."
            )

    project_root: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent.parent
    )

    @property
    def data_dir(self) -> Path:
        return self.project_root / "data"

    @property
    def pdf_dir(self) -> Path:
        return self.data_dir / "pdfs"

    @property
    def metadata_dir(self) -> Path:
        return self.data_dir / "metadata"

    @property
    def text_dir(self) -> Path:
        return self.data_dir / "text"

    request_delay_sec: float = field(
        default_factory=lambda: float(os.getenv("KAP_REQUEST_DELAY_SEC", "1.0"))
    )
    download_timeout_sec: float = field(
        default_factory=lambda: float(os.getenv("KAP_DOWNLOAD_TIMEOUT_SEC", "60.0"))
    )
    kap_max_retries: int = field(
        default_factory=lambda: int(os.getenv("KAP_MAX_RETRIES", "4"))
    )
    kap_retry_backoff_sec: float = field(
        default_factory=lambda: float(os.getenv("KAP_RETRY_BACKOFF_SEC", "2.0"))
    )

    kap_base_url: str = field(
        default_factory=lambda: os.getenv("KAP_BASE_URL", "https://www.kap.org.tr").rstrip("/")
    )
    kap_language: str = field(
        default_factory=lambda: os.getenv("KAP_LANGUAGE", "tr").strip() or "tr"
    )
    kap_download_extensions: tuple[str, ...] = field(
        default_factory=lambda: tuple(
            ext.strip().lower()
            for ext in os.getenv("KAP_DOWNLOAD_EXTENSIONS", ".pdf").split(",")
            if ext.strip()
        )
    )

    embedding_model: str = "BAAI/bge-m3"
    embedding_dim: int = 1024
    embedding_batch_size: int = 16

    chunk_size: int = 800
    chunk_overlap: int = 150
    min_chunk_chars: int = 100

    qdrant_url: str | None = field(
        default_factory=lambda: os.getenv("QDRANT_URL")
    )
    qdrant_api_key: str | None = field(
        default_factory=lambda: os.getenv("QDRANT_API_KEY")
    )
    qdrant_collection: str = field(
        default_factory=lambda: os.getenv("QDRANT_COLLECTION", "kap_bist30")
    )

    qdrant_prefer_grpc: bool = False

    def make_dirs(self) -> None:
        for d in [self.data_dir, self.pdf_dir, self.metadata_dir, self.text_dir]:
            d.mkdir(parents=True, exist_ok=True)

    @property
    def using_cloud(self) -> bool:
        return bool(self.qdrant_url and self.qdrant_api_key)


CONFIG = Config()
