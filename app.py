import json
from pathlib import Path

import streamlit as st

from jurisprudence import load_jurisprudence, precedent_weight, validate_case
from legal_engine import freshness_label, search, source_domain, validate_record
from land_verification import LAND_CHECKS, red_flags

ROOT = Path(__file__).parent
DATA = ROOT / "data" / "laws.json"


@st.cache_data
def load_laws():
    return json.loads(DATA.read_text(encoding="utf-8"))


st.set_page_config(page_title="LAWYER LAILY | Bangladesh Legal Research", page_icon="⚖️", layout="wide")
st.title("⚖️ LAWYER LAILY")
st.caption("Bangladesh legal research · বাংলাদেশ আইন অনুসন্ধান · source-grounded prototype")
st.warning(
    "Research aid only. This system is not a lawyer, judge, advocate, or filing service. "
    "Confirm current law, amendments, jurisdiction, limitation, and procedure with an enrolled Bangladesh advocate."
)

with st.sidebar:
    st.header("Research controls")
    query = st.text_input("Search law, section, subject, or Bangla term")
    status = st.selectbox("Legal status", ["All", "repealed", "unverified", "in_force_verified"])
    show_unverified = st.checkbox("Show unverified records", value=True)
    st.caption("Results never replace the official instrument or a lawyer's review.")

records = load_laws()
if not show_unverified:
    records = [record for record in records if record.get("status") == "in_force_verified"]
results = search(records, query, status)

st.metric("Catalog records", len(records))
st.caption("This is a source registry demonstration, not the complete body of Bangladesh law.")

if query and not results:
    st.info("No grounded match was found. Do not infer that no law applies; consult the official sources.")

for result in results:
    act = result.record
    errors = validate_record(act)
    with st.expander(f"{act['title']} ({act.get('year', 'n.d.')}) — {act.get('status', 'unknown')}"):
        st.write("**Act number:**", act.get("act_number") or "Pending verification")
        st.write("**Primary source:**", f"[{source_domain(act.get('source_url', ''))}]({act.get('source_url', '')})")
        st.write("**Freshness:**", freshness_label(act))
        st.write("**Verification:**", act.get("verification_note", "No verification note."))
        if errors:
            st.error("Metadata requires review: " + " ".join(errors))
        sections = result.matched_sections if query else tuple(act.get("sections", []))
        if query and not sections:
            st.caption("The match is in the instrument metadata; inspect the complete official text.")
        for section in sections:
            st.subheader(f"Section {section['number']}: {section['heading']}")
            st.write("**Plain-language commentary:**", section["explanation"])
            st.write("**Illustrative example:**", section.get("example", "Not supplied."))
            st.markdown(f"[Read the official section]({section['source_url']})")
        if not act.get("sections"):
            st.info("Sections are not yet ingested or verified. Follow the official link for the authoritative text.")

st.divider()
st.header("Bangladesh land verification workflow")
st.write("Use separate official records for each question. A portal match is a lead for verification, not conclusive title proof.")
for step in LAND_CHECKS:
    with st.expander(step.title):
        st.write("**Purpose:**", step.purpose)
        st.write("**Official service:**", f"[{step.official_url}]({step.official_url})")
        st.write("**Collect:**", ", ".join(step.user_evidence))
        st.warning(step.limitations)

st.subheader("Red flags requiring human review")
for flag in red_flags():
    st.write(f"- {flag}")

st.divider()
st.header("Jurisprudence and lawyer reasoning")
case_data = load_jurisprudence()
st.write("**Jurisprudence records:**", len(case_data.get("records", [])))
st.caption("Judgments require review of court hierarchy, material facts, issues, holding, ratio, disposition, later history, and exact citation before reliance.")
st.write("**Reasoning sequence:** clarify facts → identify issues → retrieve current law → analyze precedent → test counterarguments → map procedure and remedies → draft with review flags.")
for case in case_data.get("records", []):
    errors = validate_case(case)
    st.write(f"**{case.get('case_name', 'Unnamed case')}** — {precedent_weight(case)}")
    if errors:
        st.error("Case record requires review: " + ", ".join(errors))

st.divider()
st.header("Document drafting safety")
st.write(
    "Drafts such as GD/FIR applications, petitions, affidavits, deeds, contracts, tax/VAT submissions, and appeals "
    "must be generated only from verified templates and user-provided facts. The final document requires review, "
    "signature, court/authority formatting, limitation checks, and submission by the responsible person or advocate."
)
st.checkbox("I understand that a generated draft is not legal advice or a filed document.")
st.caption("Primary source network: bdlaws.minlaw.gov.bd · supremecourt.gov.bd · dpp.gov.bd · nbr.gov.bd")
