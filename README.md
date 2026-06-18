# Fact Check Agent

A CLI tool that fact-checks claims by searching the web and analyzing evidence with an LLM.

## How it works

1. You provide a claim (text or file).
2. The agent searches the web for relevant sources.
3. An LLM reviews the sources and returns a structured verdict.

## Setup

```bash
cd ~/Desktop/fact-check-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Add your OpenAI API key to `.env`:

```
OPENAI_API_KEY=sk-...
```

## Usage

Check a claim from the command line:

```bash
fact-check "Coffee is the most consumed beverage in the world"
```

Or run as a module:

```bash
python -m fact_check_agent "Coffee is the most consumed beverage in the world"
```

Read a claim from a file:

```bash
fact-check -f claim.txt
```

Get JSON output:

```bash
fact-check --json "The Great Wall of China is visible from space"
```

Adjust how many sources to gather:

```bash
fact-check -n 12 "Vaccines cause autism"
```

## Output

The agent returns:

- **Verdict** — `true`, `mostly_true`, `mixed`, `mostly_false`, `false`, or `unverifiable`
- **Confidence** — 0–100%
- **Summary** — short explanation for a general audience
- **Reasoning** — evidence-based analysis
- **Sources** — URLs used in the review

## Notes

- Results depend on search quality and the sources found. Treat output as a starting point, not a final authority.
- Requires network access and a valid `OPENAI_API_KEY`.
- Optional: set `OPENAI_MODEL` in `.env` (default: `gpt-4o-mini`).
