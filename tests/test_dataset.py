import json
from datetime import date, timedelta
from pathlib import Path

from legal_engine import freshness_label, search, validate_record
from land_verification import LAND_CHECKS, red_flags, validate_land_checks

ROOT = Path(__file__).parents[1]


def test_dataset_has_traceable_sources():
    records = json.loads((ROOT / "data" / "laws.json").read_text(encoding="utf-8"))
    assert records
    for record in records:
        assert record["source_url"].startswith("https://")
        assert record["status"] in {"unverified", "repealed", "in_force_verified"}
        assert record["retrieved_on"]
        for section in record.get("sections", []):
            assert section["source_url"].startswith("https://")
            assert section["number"] and section["explanation"]


def test_search_matches_section_and_status():
    records = json.loads((ROOT / "data" / "laws.json").read_text(encoding="utf-8"))
    results = search(records, "consideration", "unverified")
    assert results
    assert results[0].record["title"] == "The Contract Act, 1872"
    assert any(section["number"] == "23" for section in results[0].matched_sections)


def test_validation_and_freshness():
    records = json.loads((ROOT / "data" / "laws.json").read_text(encoding="utf-8"))
    assert validate_record(records[0]) == []
    assert freshness_label(records[0])


def test_land_workflow_has_separate_official_checks():
    titles = {step.title for step in LAND_CHECKS}
    assert {"Mutation / নামজারি", "Land development tax / দাখিলা", "Mouza map and field measurement"} <= titles
    assert all(step.official_url.startswith("https://") for step in LAND_CHECKS)
    assert validate_land_checks() == []
    assert red_flags()


def test_future_retrieval_date_is_not_called_fresh():
    future = (date.today() + timedelta(days=1)).isoformat()
    assert freshness_label({"retrieved_on": future}) == "Future retrieval date — requires review"
