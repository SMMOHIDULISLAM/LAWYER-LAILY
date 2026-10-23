# ⚖️ LAWYER LAILY

Bangladesh legal knowledge platform with two planned products: an AI legal research agent and an AI-powered mobile application.

## Run the research prototype

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The current application is a source-grounded legal research prototype with a versioned law catalog, jurisprudence-record validation, reasoning-policy safeguards, and a Bangladesh land-verification checklist. It is not a complete body of Bangladesh or international law, a comprehensive case database, a trained general-purpose AI agent, or a mobile app.

- [Project scope](docs/PROJECT_SCOPE.md)
- [Source network](docs/SOURCE_NETWORK.md)
- [Original legal source registry](data/sources.json)
- [Structured source registry](data/source_registry.json)
- [Reasoning policy](data/reasoning_policy.json)

## Jurisprudence and lawyer reasoning

BDLAYS is being prepared to reason like a careful Bangladesh legal researcher: clarify facts, identify issues, locate current primary law, analyze verified precedents, test both sides, map procedure and remedies, and disclose uncertainty.

Judgments are not training examples merely because they appear online. Each case record must contain the court, date, exact citation, source URL, procedural history, material facts, issues, holding, ratio, disposition, precedent scope, later history, verification state, and retrieval date. The empty initial corpus is intentional; no invented case law is permitted.

This system must not claim to be a lawyer, judge, advocate, or government officer; decide disputed facts; pronounce a verdict; guarantee legal outcomes; or replace local professional review. It must cite authoritative sources or label an answer unresolved and show jurisdiction, effective date, and verification state.

## Accuracy and coverage principles

Never fabricate statutes, articles, case citations, HS codes, customs rates, tax dates, procedures, or outcomes. Official sources must be checked for current text, amendments, commencement, repeal, jurisdiction, access permissions, and retrieval date. Commentary must remain separate from primary law. Country-by-country expansion for customs, taxes, import/export policy, business law, and international law is a future versioned-corpus and source-monitoring program—not a claim of 100% coverage or accuracy in this prototype.
