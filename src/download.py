from __future__ import annotations

import json
import logging
import re
import time
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urljoin

import httpx

from .bist30 import BIST30_TICKERS
from .config import CONFIG

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("download")


class KapWebError(RuntimeError):
    """KAP web çağrısı beklenen şekilde dönmedi."""


def safe_filename(name: str) -> str:
    keep = "-_.() "
    cleaned = "".join(c if c.isalnum() or c in keep else "_" for c in name)
    return re.sub(r"\s+", " ", cleaned).strip()[:140] or "attachment.pdf"


def should_download(filename: str) -> bool:
    if not CONFIG.kap_download_extensions:
        return True
    return filename.lower().endswith(CONFIG.kap_download_extensions)


def as_list(payload: Any) -> list[dict]:
    if payload is None:
        return []
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("items", "data", "result", "results", "content", "list", "disclosures"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [payload]
    return []


def localized_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return value.get("tr") or value.get("TR") or value.get("default") or value.get("en") or ""
    return str(value)


def parse_datetime(value: Any) -> datetime | None:
    if not value:
        return None

    text = str(value).strip()
    if not text:
        return None

    normalized = text.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        pass

    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y.%m.%d %H:%M:%S",
        "%d.%m.%Y %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
        "%Y-%m-%d",
        "%Y.%m.%d",
        "%d.%m.%Y",
        "%d/%m/%Y",
    ):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue

    return None


def in_config_date_range(dt: datetime | None) -> bool:
    if dt is None:
        log.debug("Tarih parse edilemedi, bildirim tarih aralığı dışında sayılıyor.")
        return False
    day = dt.date()
    return CONFIG.start_date <= day <= CONFIG.end_date


def parse_int(value: Any) -> int | None:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


def split_stock_codes(value: Any, fallback: str) -> list[str]:
    if not value:
        return [fallback]
    if isinstance(value, list):
        return [str(item.get("code") if isinstance(item, dict) else item) for item in value if item]
    return [token for token in re.split(r"[^A-Z0-9]+", str(value).upper()) if token] or [fallback]


def clean_link_text(value: str) -> str:
    without_tags = re.sub(r"<[^>]+>", "", value)
    return unescape(without_tags).strip()


class KapWebClient:
    def __init__(self, http: httpx.Client):
        self.http = http

    def _url(self, path_or_url: str) -> str:
        if path_or_url.startswith(("http://", "https://")):
            return path_or_url
        return urljoin(f"{CONFIG.kap_base_url.rstrip('/')}/", path_or_url.lstrip("/"))

    def request(self, method: str, path_or_url: str, **kwargs: Any) -> httpx.Response:
        url = self._url(path_or_url)
        last_exc: Exception | None = None
        for attempt in range(1, CONFIG.kap_max_retries + 1):
            try:
                resp = self.http.request(
                    method,
                    url,
                    timeout=CONFIG.download_timeout_sec,
                    follow_redirects=True,
                    **kwargs,
                )
                if resp.status_code in {429, 500, 502, 503, 504} and attempt < CONFIG.kap_max_retries:
                    delay = CONFIG.kap_retry_backoff_sec * attempt
                    log.warning(
                        "  KAP %s döndü, tekrar denenecek (%d/%d): %s",
                        resp.status_code,
                        attempt,
                        CONFIG.kap_max_retries,
                        url,
                    )
                    time.sleep(delay)
                    continue
                return resp
            except (
                httpx.RemoteProtocolError,
                httpx.ReadTimeout,
                httpx.ConnectTimeout,
                httpx.ConnectError,
                httpx.WriteError,
                httpx.ProtocolError,
            ) as exc:
                last_exc = exc
                if attempt >= CONFIG.kap_max_retries:
                    break
                delay = CONFIG.kap_retry_backoff_sec * attempt
                log.warning(
                    "  KAP bağlantısı koptu, tekrar denenecek (%d/%d): %s",
                    attempt,
                    CONFIG.kap_max_retries,
                    url,
                )
                time.sleep(delay)

        raise KapWebError(f"KAP isteği başarısız: {url} ({last_exc})")

    def get_text(self, path_or_url: str) -> str:
        resp = self.request("GET", path_or_url)
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise KapWebError(f"KAP sayfası alınamadı {resp.status_code}: {resp.text[:300]}") from exc
        return resp.text

    def search_page_html(self) -> str:
        return self.get_text(f"/{CONFIG.kap_language}/bildirim-sorgu?srcbar=Y")

    def members_by_ticker(self, tickers: Iterable[str]) -> dict[str, dict]:
        html = self.search_page_html()
        found: dict[str, dict] = {}
        for ticker in tickers:
            member = self._member_from_search_html(html, ticker)
            if member:
                found[ticker] = member
        return found

    @staticmethod
    def _member_from_search_html(html: str, ticker: str) -> dict | None:
        for match in re.finditer(re.escape(ticker), html):
            start = html.rfind('{\\"kapMemberOid\\"', 0, match.start())
            escaped = True
            if start < 0:
                start = html.rfind('{"kapMemberOid"', 0, match.start())
                escaped = False
            if start < 0:
                continue

            # Parantez sayacıyla JSON nesnesinin gerçek kapanış brace'ini bul
            raw_html = html[start:]
            if escaped:
                raw_html = raw_html.replace('\\"', '"')
            depth = 0
            end_pos = -1
            for i, ch in enumerate(raw_html):
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        end_pos = i
                        break
            if end_pos < 0:
                continue

            raw = raw_html[: end_pos + 1]
            try:
                member = json.loads(raw)
            except json.JSONDecodeError:
                continue

            if ticker in split_stock_codes(member.get("stockCode"), ticker):
                return member

        return None

    def disclosures(self, member: dict) -> list[dict]:
        payload = {
            "fromDate": CONFIG.start_date.isoformat(),
            "toDate": CONFIG.end_date.isoformat(),
            "memberType": member.get("kapMemberType") or "IGS",
            "mkkMemberOidList": [member["mkkMemberOid"]],
            "inactiveMkkMemberOidList": [],
            "disclosureClass": "",
            "subjectList": [],
            "isLate": "",
            "mainSector": "",
            "sector": "",
            "subSector": "",
            "marketOid": "",
            "index": "",
            "bdkReview": "",
            "bdkMemberOidList": [],
            "year": "",
            "term": "",
            "ruleType": "",
            "period": "",
            "fromSrc": False,
            "srcCategory": "",
            "disclosureIndexList": [],
        }
        resp = self.request(
            "POST",
            f"/{CONFIG.kap_language}/api/disclosure/members/byCriteria",
            json=payload,
        )
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise KapWebError(f"KAP bildirim sorgusu hata verdi {resp.status_code}: {resp.text[:300]}") from exc
        try:
            return as_list(resp.json())
        except json.JSONDecodeError as exc:
            raise KapWebError(f"KAP bildirim sorgusu JSON dönmedi: {resp.text[:300]}") from exc

    def detail_attachments(self, disclosure_index: int) -> list[dict]:
        html = self.get_text(f"/{CONFIG.kap_language}/Bildirim/{disclosure_index}")
        attachments: list[dict] = []
        seen: set[str] = set()

        pattern = re.compile(
            r'href="(?P<url>[^"]*/api/file/download/(?P<id>[^"]+))"[^>]*>'
            r"(?P<name>.*?)</a>",
            re.IGNORECASE | re.DOTALL,
        )
        for match in pattern.finditer(html):
            url = unescape(match.group("url"))
            file_name = clean_link_text(match.group("name")) or f"{match.group('id')}.pdf"
            if url.startswith("/"):
                url = self._url(url)
            if url in seen:
                continue
            seen.add(url)
            attachments.append({"url": url, "filename": file_name})

        return attachments

    def download_pdf(self, url_or_path: str, out_path: Path) -> bool:
        if out_path.exists() and out_path.stat().st_size > 0:
            log.debug("  Zaten var, atlıyorum: %s", out_path.name)
            return True

        try:
            resp = self.request("GET", url_or_path)
        except KapWebError as exc:
            log.warning("  Dosya indirilemedi, atlandı: %s (%s)", url_or_path, exc)
            return False
        if resp.status_code == 404:
            log.warning("  Dosya bulunamadı: %s", url_or_path)
            return False
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            log.warning("  Dosya indirilemedi (%s): %s", url_or_path, exc)
            return False

        content_type = resp.headers.get("content-type", "")
        if not resp.content.startswith(b"%PDF") and "pdf" not in content_type.lower():
            log.warning("  PDF olmayan dosya atlandı: %s (%s)", url_or_path, content_type)
            return False

        out_path.write_bytes(resp.content)
        return True


def serialize_disclosure(ticker: str, member: dict, summary: dict) -> dict:
    index = parse_int(summary.get("disclosureIndex")) or summary.get("disclosureIndex")
    publish_dt = parse_datetime(summary.get("publishDate"))
    stock_codes = split_stock_codes(summary.get("stockCodes") or summary.get("relatedStocks"), ticker)

    return {
        "index": index,
        "publish_datetime": publish_dt.isoformat() if publish_dt else str(summary.get("publishDate") or ""),
        "company_name": summary.get("kapTitle") or member.get("kapMemberTitle") or "",
        "fund_code": summary.get("fundCode"),
        "stock_codes": stock_codes,
        "subject": localized_text(summary.get("subject")),
        "summary": localized_text(summary.get("summary")),
        "disclosure_type": summary.get("disclosureType") or summary.get("disclosureClass") or "",
        "disclosure_class": summary.get("disclosureClass") or "",
        "has_attachment": bool(summary.get("attachmentCount")),
        "attachment_count": summary.get("attachmentCount") or 0,
        "is_late": bool(summary.get("isLate")),
        "is_corrective": bool(summary.get("modifyStatus")),
        "is_english": False,
        "has_multi_language_support": bool(summary.get("hasMultiLanguageSupport")),
        "url": f"{CONFIG.kap_base_url.rstrip('/')}/{CONFIG.kap_language}/Bildirim/{index}",
        "ticker": ticker,
        "company_oid": member.get("kapMemberOid"),
        "mkk_member_oid": member.get("mkkMemberOid"),
        "kap_company_code": member.get("companyCode"),
        "source": "kap_web",
        "attachments": [],
    }


def add_attachment(record: dict, file_name: str, url: str, out_path: Path) -> None:
    record["attachments"].append(
        {
            "filename": file_name,
            "local_path": str(out_path.relative_to(CONFIG.project_root)),
            "url": url,
        }
    )


def fetch_one_company(client: KapWebClient, ticker: str, member: dict) -> dict:
    log.info("-> %s işleniyor... (%s)", ticker, member.get("kapMemberTitle"))

    meta_records: list[dict] = []
    pdf_dir_company = CONFIG.pdf_dir / ticker
    pdf_dir_company.mkdir(parents=True, exist_ok=True)

    summaries = client.disclosures(member)
    log.info("  %d bildirim bulundu", len(summaries))

    pdf_count = 0
    seen_indices: set[int] = set()

    for summary in summaries:
        parsed_index = parse_int(summary.get("disclosureIndex"))
        if parsed_index is None or parsed_index in seen_indices:
            continue
        seen_indices.add(parsed_index)

        publish_dt = parse_datetime(summary.get("publishDate"))
        if not in_config_date_range(publish_dt):
            continue

        record = serialize_disclosure(ticker, member, summary)

        notification_name = f"{parsed_index}_KAP_Bildirim.pdf"
        notification_path = pdf_dir_company / notification_name
        notification_url = f"/{CONFIG.kap_language}/api/BildirimPdf/{parsed_index}"
        if client.download_pdf(notification_url, notification_path):
            add_attachment(record, "KAP Bildirim PDF", client._url(notification_url), notification_path)
            pdf_count += 1

        if summary.get("attachmentCount"):
            try:
                attachments = client.detail_attachments(parsed_index)
            except KapWebError as exc:
                log.warning("  Ek dosyalar okunamadı (index=%s): %s", parsed_index, exc)
                attachments = []

            for attachment in attachments:
                file_name = attachment["filename"]
                if not should_download(file_name):
                    continue

                out_name = f"{parsed_index}_{safe_filename(file_name)}"
                out_path = pdf_dir_company / out_name
                if client.download_pdf(attachment["url"], out_path):
                    add_attachment(record, file_name, attachment["url"], out_path)
                    pdf_count += 1
                time.sleep(CONFIG.request_delay_sec / 2)

        meta_records.append(record)
        time.sleep(CONFIG.request_delay_sec)

    meta_path = CONFIG.metadata_dir / f"{ticker}.json"
    meta_path.write_text(
        json.dumps(meta_records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    status = "ok" if meta_records else "empty"
    log.info("  ✓ %s: %d bildirim, %d PDF indirildi", ticker, len(meta_records), pdf_count)

    return {
        "ticker": ticker,
        "status": status,
        "count": len(meta_records),
        "pdf_count": pdf_count,
    }


def run(tickers: Iterable[str] | None = None) -> list[dict]:
    CONFIG.make_dirs()
    tickers = [ticker.upper() for ticker in (list(tickers) if tickers else BIST30_TICKERS)]

    log.info("=" * 60)
    log.info("KAP web indirme başladı")
    log.info("Base URL: %s", CONFIG.kap_base_url)
    log.info("Tarih aralığı: %s -> %s", CONFIG.start_date, CONFIG.end_date)
    log.info("Hisse sayısı: %d", len(tickers))
    log.info("=" * 60)

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0 Safari/537.36",
        "Accept": "application/json, text/html, application/pdf, */*",
        "Accept-Language": CONFIG.kap_language,
        "Connection": "close",
        "Origin": CONFIG.kap_base_url,
        "Referer": f"{CONFIG.kap_base_url.rstrip('/')}/{CONFIG.kap_language}/bildirim-sorgu?srcbar=Y",
    }

    summary = []
    limits = httpx.Limits(max_connections=5, max_keepalive_connections=0)
    with httpx.Client(headers=headers, timeout=CONFIG.download_timeout_sec, limits=limits) as http:
        client = KapWebClient(http)
        members = client.members_by_ticker(tickers)
        log.info("%d/%d şirket KAP sayfasında bulundu", len(members), len(tickers))

        for ticker in tickers:
            member = members.get(ticker)
            if not member:
                log.error("  Ticker için KAP şirket kaydı bulunamadı: %s", ticker)
                summary.append({"ticker": ticker, "status": "not_found", "count": 0, "pdf_count": 0})
                continue

            try:
                res = fetch_one_company(client, ticker, member)
                summary.append(res)
            except Exception as exc:
                log.exception("Beklenmeyen hata (%s): %s", ticker, exc)
                summary.append({"ticker": ticker, "status": "exception", "count": 0, "pdf_count": 0})
            time.sleep(CONFIG.request_delay_sec)

    log.info("=" * 60)
    log.info("Özet:")
    total_disc = sum(s.get("count", 0) for s in summary)
    total_pdf = sum(s.get("pdf_count", 0) for s in summary)
    log.info("  Toplam bildirim: %d", total_disc)
    log.info("  Toplam PDF: %d", total_pdf)
    log.info("  Başarılı: %d / %d", sum(1 for s in summary if s["status"] == "ok"), len(summary))

    return summary


if __name__ == "__main__":
    run()
