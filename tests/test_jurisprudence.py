from jurisprudence import load_jurisprudence, precedent_weight, validate_case


def test_empty_jurisprudence_corpus_is_explicitly_valid():
    data = load_jurisprudence()
    assert data["records"] == []
    assert data["ingestion_policy"]["never_invent_citations"] is True


def test_case_validation_requires_provenance():
    case = {"case_name": "Example", "precedent_scope": "persuasive"}
    errors = validate_case(case)
    assert "citation" in errors
    assert "source_url" in errors
    assert precedent_weight(case) == "persuasive only"


def test_non_binding_scope_is_not_classified_as_binding():
    assert precedent_weight({"precedent_scope": "non-binding"}) == "unclassified; do not rely without review"


def test_case_validation_rejects_invalid_dates_and_hosts():
    case = {
        "case_name": "Example", "court": "Court", "jurisdiction": "BD",
        "decision_date": "2026/01/01", "citation": "1", "source_url": "https://",
        "procedural_history": "history", "material_facts": "facts", "issues": "issues",
        "holding": "holding", "ratio": "ratio", "disposition": "disposed",
        "precedent_scope": "persuasive", "later_history": "none",
        "verification_state": "unverified", "retrieved_on": "2026-01-01",
    }
    errors = validate_case(case)
    assert "source_url must use HTTPS and include a host" in errors
    assert "decision_date must be an ISO date (YYYY-MM-DD)" in errors
