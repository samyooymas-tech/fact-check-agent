# Fact Check Agent

## Overview

Fact Check Agent is a web-based application that automatically verifies factual claims found in PDF documents.

Users can upload any PDF containing statistics, dates, financial figures, market-size estimates, user counts, or other factual statements. The system extracts potential claims, searches live web sources for supporting evidence, and generates a fact-check report.

This project was developed as part of an AI Product & Engineering assessment focused on automated claim verification.

---

## Features

### PDF Upload

Upload any PDF document through a simple web interface.

### Automated Claim Extraction

The application automatically identifies potentially verifiable claims such as:

* Statistics
* Percentages
* Financial figures
* Market size estimates
* User counts
* Dates and years

### Live Web Verification

For each extracted claim, the system searches the web using Tavily Search API to retrieve relevant supporting evidence.

### Fact Check Report

The application generates a structured report containing:

* Extracted Claim
* Verification Status
* Supporting Evidence
* Explanation

---

## System Workflow

PDF Upload

↓

Text Extraction (PyMuPDF)

↓

Claim Detection

↓

Web Search (Tavily API)

↓

Evidence Collection

↓

Fact Check Report Generation

---

## Technology Stack

### Frontend

* Streamlit

### Document Processing

* PyMuPDF (fitz)

### Search & Verification

* Tavily Search API

### Data Processing

* Pandas
* Python

### Deployment

* Streamlit Community Cloud

---

## Project Structure

```text
fact-check-agent/
│
├── app.py
├── requirements.txt
├── README.md
│
└── .streamlit/
    └── secrets.toml
```

---

## Installation

```bash
git clone <repository-url>

cd fact-check-agent

pip install -r requirements.txt
```

---

## Environment Variables

Create Streamlit secrets:

```toml
TAVILY_API_KEY="your_api_key"
```

---

## Running Locally

```bash
streamlit run app.py
```

or

```bash
python3 -m streamlit run app.py
```

---

## Deployment

The application is deployed using Streamlit Community Cloud.

Deployment includes:

* Public web access
* Secure API key management
* Automatic redeployment from GitHub

---

## Example Use Cases

### Marketing Content Validation

Verify statistics and market-size claims before publication.

### Research Reports

Validate cited numbers and factual statements.

### Business Presentations

Check accuracy of financial and industry claims.

### Product Documentation

Verify technical statements using live web evidence.

---

## Future Improvements

* LLM-based reasoning layer for deeper fact verification
* Source credibility scoring
* Multi-source confidence ranking
* PDF annotation with highlighted inaccuracies
* Downloadable verification reports
* Batch document processing

---

## Disclaimer

Fact Check Agent provides automated evidence gathering and claim verification assistance. Results should be reviewed by a human before being used in legal, medical, financial, or other high-stakes contexts.
