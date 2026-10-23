from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parent
MANIFEST = ROOT / "data" / "agent_manifest.json"


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def onboarding_stages() -> list[dict[str, Any]]:
    return load_manifest()["country_onboarding_stages"]


def capability_summary() -> list[str]:
    return load_manifest()["capabilities"]


def safety_gates() -> list[str]:
    return load_manifest()["safety_gates"]
