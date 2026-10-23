from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "jurisprudence.json"

REQUIRED_FIELDS = (
    "case_name", "court", "jurisdiction", "decision_date", "citation", "source_url",
    "procedural_history", "material_facts", "issues", "holding", "ratio", "disposition",
    "precedent_scope", "later_history", "verification_state", "retrieved_on",
)
DATE_FIELDS = ("decision_date", "retrieved_on")


def load_jurisprudence() -> dict[str, Any]:
    return json.loads(DATA.read_text(encoding="utf-8"))


def validate_case(record: dict[str, Any]) -> list[str]:
    errors = [field for field in REQUIRED_FIELDS if not record.get(field)]
    source_url = str(record.get("source_url", ""))
    if source_url and (not source_url.startswith("https://") or not urlparse(source_url).netloc):
        errors.append("source_url must use HTTPS and include a host")
    for field in DATE_FIELDS:
        value = record.get(field)
        if value:
            try:
                date.fromisoformat(str(value))
            except ValueError:
                errors.append(f"{field} must be an ISO date (YYYY-MM-DD)")
    return errors


def precedent_weight(record: dict[str, Any]) -> str:
    scope = str(record.get("precedent_scope", "")).casefold().strip()
    if any(term in scope for term in ("non-binding", "non binding", "not binding")):
        return "unclassified; do not rely without review"
    if scope.startswith("binding") or scope == "binding":
        return "binding candidate, subject to court hierarchy and later history"
    if "persuasive" in scope:
        return "persuasive only"
    return "unclassified; do not rely without review"
