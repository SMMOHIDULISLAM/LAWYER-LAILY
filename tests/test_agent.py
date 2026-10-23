from agent_architecture import capability_summary, load_manifest, onboarding_stages, safety_gates


def test_bdlays_manifest_has_safety_and_country_gates():
    manifest = load_manifest()
    assert manifest["name"] == "BDLAYS"
    assert "Bangladesh" in manifest["jurisdiction_priority"]
    assert capability_summary()
    assert safety_gates()
    stages = onboarding_stages()
    assert len(stages) == 8
    assert stages[0]["name"] == "jurisdiction_definition"
    assert stages[-1]["name"] == "continuous_change_monitoring"
