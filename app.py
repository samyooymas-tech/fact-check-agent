import streamlit as st
import fitz
import re
import pandas as pd
from tavily import TavilyClient

# API Key
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

tavily = TavilyClient(api_key=TAVILY_API_KEY)

st.set_page_config(
    page_title="Fact Check Agent",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Fact Check Agent")
st.write("Upload a PDF and automatically verify claims against live web data.")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


def extract_text(pdf_file):

    doc = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    text = ""

    for page in doc:
        text += page.get_text()

    return text


def extract_claims(text):

    sentences = re.split(r'[.!?]\s+', text)

    claims = []

    for sentence in sentences:

        if (
            "%" in sentence
            or "$" in sentence
            or re.search(r"\b(19|20)\d{2}\b", sentence)
            or "million" in sentence.lower()
            or "billion" in sentence.lower()
            or "trillion" in sentence.lower()
        ):

            sentence = sentence.strip()

            if len(sentence) > 20:
                claims.append(sentence)

    return claims[:10]


def verify_claim(claim):

    try:

        results = tavily.search(
            query=claim,
            search_depth="basic",
            max_results=5
        )

        if len(results["results"]) == 0:

            return {
                "status": "False",
                "correct_fact": "No supporting evidence found",
                "reason": "No relevant web evidence"
            }

        evidence_text = ""

        for result in results["results"]:
            evidence_text += result["content"] + " "

        evidence_text = evidence_text[:500]

        return {
            "status": "Verified",
            "correct_fact": evidence_text,
            "reason": "Supporting web evidence found"
        }

    except Exception as e:

        return {
            "status": "Error",
            "correct_fact": "",
            "reason": str(e)
        }


if uploaded_file:

    with st.spinner("Reading PDF..."):
        text = extract_text(uploaded_file)

    with st.spinner("Extracting claims..."):
        claims = extract_claims(text)

    if len(claims) == 0:

        st.warning(
            "No statistical or numerical claims detected."
        )

        st.stop()

    st.success(
        f"Found {len(claims)} potential claims"
    )

    rows = []

    for claim in claims:

        with st.spinner(
            f"Checking claim..."
        ):

            result = verify_claim(claim)

            rows.append(
                {
                    "Claim": claim,
                    "Status": result["status"],
                    "Correct Fact": result["correct_fact"],
                    "Reason": result["reason"]
                }
            )

    df = pd.DataFrame(rows)

    st.subheader("Fact Check Report")

    st.dataframe(
        df,
        use_container_width=True
    )
