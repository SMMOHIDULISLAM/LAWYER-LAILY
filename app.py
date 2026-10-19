"""LAWYER LAILY — source discovery prototype. Not a legal advice system."""
import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="LAWYER LAILY", page_icon="⚖️", layout="wide")
st.title("⚖️ LAWYER LAILY | লইয়ার লাইলী")
st.caption("Bangladesh AI Legal Agent + Mobile App — source-directory prototype")
st.warning("This prototype lists reference portals only. It does not yet retrieve case records or generate verified legal advice.")
sources = json.loads((Path(__file__).parent / "data" / "sources.json").read_text(encoding="utf-8"))
query = st.text_input("Search legal source / উৎস খুঁজুন")
categories = sorted({s["category"] for s in sources})
category = st.selectbox("Category", ["All"] + categories)
filtered = [s for s in sources if (category == "All" or s["category"] == category) and (not query or query.casefold() in (s["name"] + " " + s["category"] + " " + s["authority"]).casefold())]
st.metric("Sources in directory", len(filtered))
for s in filtered:
    with st.container(border=True):
        st.subheader(s["name"])
        st.write(f"**Type:** {s['category']}  |  **Authority:** {s['authority']}  |  **Access:** {s['access']}")
        st.link_button("Visit official / source portal", s["url"])
st.divider()
st.subheader("AI legal assistant — planned")
st.info("RAG-based law, court-order and policy answers will be added after verified text ingestion and citation testing.")
st.subheader("Nationwide court dashboard — planned")
st.markdown("[Supreme Court](https://www.supremecourt.gov.bd/) · [District e-Cause List](https://causelist.judiciary.gov.bd/)")
