from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Iterable
from urllib.parse import urlparse


@dataclass(frozen=True)
class SearchResult:
    record: dict[str, Any]
    matched_sections: tuple[dict[str, Any], ...]
    score: int


def _haystack(record: dict[str, Any]) -> str:
    parts = [record.get("title", ""), str(record.get("year", "")), record.get("act_number", "")]
    parts.extend(record.get("keywords", []))
    for section in record.get("sections", []):
        parts.extend([section.get("number", ""), section.get("heading", ""), section.get("explanation", "")])
    return " ".join(str(part) for part in parts).casefold()


def search(records: Iterable[dict[str, Any]], query: str, status: str = "All") -> list[SearchResult]:
    normalized = (query or "").strip().casefold()
    results: list[SearchResult] = []
    for record in records:
        if status != "All" and record.get("status") != status:
            continue
        sections = tuple(record.get("sections", []))
        if not normalized:
            results.append(SearchResult(record, sections, 0))
            continue
        title_match = normalized in str(record.get("title", "")).casefold()
        matching_sections = tuple(section for section in sections if normalized in " ".join(str(value) for value in section.values()).casefold())
        if title_match or normalized in _haystack(record):
            score = (100 if title_match else 0) + (10 * len(matching_sections))
            results.append(SearchResult(record, matching_sections, score))
    return sorted(results, key=lambda result: (-result.score, result.record.get("title", "")))


def validate_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not record.get("source_url", "").startswith("https://"):
        errors.append("Record is missing an HTTPS source URL.")
    if record.get("status") not in {"unverified", "repealed", "in_force_verified"}:
        errors.append("Record has an unsupported legal status.")
    if not record.get("retrieved_on"):
        errors.append("Record has no retrieval date.")
    for section in record.get("sections", []):
        if not section.get("source_url", "").startswith("https://"):
            errors.append(f"Section {section.get('number', '?')} is missing an HTTPS source URL.")
        if not section.get("explanation"):
            errors.append(f"Section {section.get('number', '?')} has no explanation.")
    return errors


def freshness_label(record: dict[str, Any]) -> str:
    retrieved = record.get("retrieved_on")
    if not retrieved:
        return "Unknown freshness"
    try:
        age = (date.today() - date.fromisoformat(retrieved)).days
    except ValueError:
        return "Invalid retrieval date"
    if age < 0:
        return "Future retrieval date — requires review"
    if age <= 7:
        return "Checked within 7 days"
    if age <= 30:
        return "Checked within 30 days"
    return f"Last checked {age} days ago"


def source_domain(url: str) -> str:
    return urlparse(url).netloc or "unknown source"
