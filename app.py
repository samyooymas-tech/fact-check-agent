import streamlit as st
import fitz
import json
import pandas as pd
import google.generativeai as genai
from tavily import TavilyClient

# API Keys
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

tavily = TavilyClient(api_key=TAVILY_API_KEY)

st.set_page_config(
    page_title="Fact Check Agent",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Fact Check Agent")
st.write("Upload a PDF and verify factual claims using live web data.")

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

    prompt = f"""
    Extract only externally verifiable factual claims.

    INCLUDE:
    - market sizes
    - statistics
    - percentages
    - revenue figures
    - funding amounts
    - user counts
    - growth rates
    - industry reports

    IGNORE:
    - names
    - addresses
    - resumes
    - employment dates
    - education history
    - internship details
    - project timelines

    Return ONLY a JSON array.

    Example:

    [
      "The global AI market will reach $1.8 trillion by 2030",
      "OpenAI has over 500 million weekly active users"
    ]

    TEXT:
    {text[:8000]}
    """

    try:

        response = model.generate_content(prompt)

        claims = response.text

        claims = claims.replace("```json", "")
        claims = claims.replace("```", "")

        claims = json.loads(claims)

        # Limit to avoid quota issues
        return claims[:3]

    except Exception as e:

        st.error(f"Claim extraction failed: {e}")

        return []


def verify_claim(claim):

    try:

        search_results = tavily.search(
            query=claim,
            search_depth="basic",
            max_results=3
        )

        evidence = ""

        for result in search_results["results"]:
            evidence += result["content"] + "\n"

        prompt = f"""
        Claim:
        {claim}

        Evidence:
        {evidence}

        Determine whether the claim is:

        Verified
        Inaccurate
        False

        Return ONLY JSON.

        {{
            "status":"Verified",
            "correct_fact":"...",
            "reason":"..."
        }}
        """

        result = model.generate_content(prompt)

        txt = result.text

        txt = txt.replace("```json", "")
        txt = txt.replace("```", "")

        return json.loads(txt)

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

        st.warning("No verifiable claims found.")

        st.stop()

    st.success(f"Found {len(claims)} claims")

    rows = []

    for claim in claims:

        with st.spinner(f"Checking: {claim[:60]}..."):

            result = verify_claim(claim)

            rows.append({
                "Claim": claim,
                "Status": result.get("status", ""),
                "Correct Fact": result.get("correct_fact", ""),
                "Reason": result.get("reason", "")
            })

    df = pd.DataFrame(rows)

    st.subheader("Fact Check Report")

    st.dataframe(
        df,
        use_container_width=True
    )