"""Check configured official source endpoints and write a retrieval report.

This command intentionally does not scrape, rewrite, or mark legal records as verified.
Human/legal-editor review is required before importing text or changing legal status.
"""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "source_registry.json"
REPORT = ROOT / "data" / "source_health.json"


def check(url: str) -> dict[str, object]:
    request = Request(url, headers={"User-Agent": "LAWYER-LAILY-source-check/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            return {"reachable": True, "status": response.status, "content_type": response.headers.get_content_type()}
    except HTTPError as error:
        return {"reachable": False, "status": error.code, "error": "http_error"}
    except (URLError, TimeoutError, OSError) as error:
        return {"reachable": False, "error": type(error).__name__}


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    checked_at = datetime.now(UTC).isoformat()
    report = {
        "checked_at": checked_at,
        "policy": "Endpoint health only; no legal content or status is verified automatically.",
        "sources": [{**source, "check": check(source["url"])} for source in registry],
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT} with {len(report['sources'])} endpoint checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
