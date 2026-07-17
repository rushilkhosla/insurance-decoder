"""Insurance Decoder — upload an Indian insurance policy PDF, get a plain-language
breakdown of what you actually bought.

MVP scope: Motor (car/bike) and Health insurance. Output in English or Hindi.

Pipeline: extract text from the PDF (pypdf) -> send to Claude with a structured
prompt -> render sections: summary, what's covered, what's NOT covered, limits &
waiting periods, red flags, jargon glossary, questions to ask your agent.
"""
import json
import os
import re

from flask import Flask, jsonify, render_template, request
from pypdf import PdfReader

app = Flask(__name__)

PORT = 8523
MAX_POLICY_CHARS = 150_000  # ~40k tokens; enough for any retail policy wording

ALLOWED_ORIGINS = {
    "https://sevenfigurewealth.in",
    "https://www.sevenfigurewealth.in",
}


@app.after_request
def add_cors_headers(response):
    origin = request.headers.get("Origin")
    if origin in ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/analyze", methods=["OPTIONS"])
def analyze_preflight():
    return "", 204


def load_api_key():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        for line in open(env_path):
            m = re.match(r"\s*ANTHROPIC_API_KEY\s*=\s*(.+)", line)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    return None


SYSTEM_PROMPT = """You are an expert on Indian retail insurance (IRDAI-regulated) who explains \
policies to ordinary buyers. You are NOT a licensed advisor: never recommend buying, \
switching, or cancelling a policy — only explain what the document says and what to verify. \
Be blunt about traps. Use simple words a 15-year-old understands. Amounts in ₹ (Indian format). \
If the document is not an insurance policy, say so in the "error" field."""

ANALYSIS_PROMPT = """The user bought or is considering this {policy_type} insurance policy. \
Analyze the policy document text below and reply in {language}.

Return ONLY valid JSON with this exact shape:
{{
  "error": null or "reason this can't be analyzed",
  "policy_name": "product + insurer name if found",
  "policy_type_detected": "motor / health / other",
  "summary": "3-4 sentences: what this policy is, what it fundamentally does and doesn't do",
  "covered": [{{"item": "...", "detail": "plain-language explanation with amounts"}}],
  "not_covered": [{{"item": "...", "detail": "exclusion explained plainly, why claims get rejected on this"}}],
  "limits": [{{"item": "...", "detail": "waiting periods, sub-limits, room-rent caps, co-pay, deductibles, depreciation, IDV — with numbers"}}],
  "red_flags": [{{"severity": "high/medium/low", "flag": "...", "detail": "why this could hurt the buyer at claim time"}}],
  "jargon": [{{"term": "...", "meaning": "one-line plain explanation"}}],
  "questions": ["specific questions the buyer should ask their agent/insurer before or after buying"]
}}

Rules:
- Everything grounded in the document text; if a standard clause (e.g. health waiting periods, motor depreciation slabs) is expected but MISSING from the text, flag that as a question, don't invent numbers.
- red_flags: focus on what causes claim rejection or payout shrinkage in India (room-rent proportionate deduction, disease sub-limits, consumables, zero-dep absent, PYP disclosure, NCB rules).
- If language is Hindi, write values in Hindi (Devanagari) but keep insurance terms with the English term in brackets, e.g. "प्रतीक्षा अवधि (waiting period)".

POLICY DOCUMENT TEXT:
{text}"""


def extract_pdf_text(file_storage):
    reader = PdfReader(file_storage)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


@app.route("/")
def index():
    return render_template("index.html", have_key=bool(load_api_key()))


@app.route("/analyze", methods=["POST"])
def analyze():
    key = load_api_key()
    if not key:
        return jsonify(error="No ANTHROPIC_API_KEY found. Add it to your shell env or put "
                             "ANTHROPIC_API_KEY=sk-... in a .env file next to app.py."), 500

    f = request.files.get("policy")
    if not f:
        return jsonify(error="No file uploaded."), 400
    policy_type = request.form.get("policy_type", "health")
    language = "Hindi" if request.form.get("language") == "hi" else "English"

    try:
        if f.filename.lower().endswith(".pdf"):
            text = extract_pdf_text(f)
        else:
            text = f.read().decode("utf-8", errors="replace")
    except Exception as e:
        return jsonify(error=f"Could not read the file: {e}"), 400

    text = text.strip()
    if len(text) < 200:
        return jsonify(error="Couldn't extract readable text from this PDF. It may be a "
                             "scanned image — try the original digital PDF from the insurer."), 400
    text = text[:MAX_POLICY_CHARS]

    import anthropic
    client = anthropic.Anthropic(api_key=key)
    try:
        msg = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": ANALYSIS_PROMPT.format(
                policy_type=policy_type, language=language, text=text)}],
        )
    except anthropic.APIError as e:
        return jsonify(error=f"Claude API error: {e}"), 502

    raw = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")

    if msg.stop_reason == "max_tokens":
        app.logger.error("Response truncated at max_tokens (input was %d chars)", len(text))
        return jsonify(error="Your policy document is long enough that the analysis got cut off "
                             "mid-way. Try again — if it keeps happening, this document needs a "
                             "longer output limit than the app currently allows."), 502

    # Strip markdown code fences (```json ... ```) some responses wrap JSON in.
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", raw, re.DOTALL)
    candidate = fence.group(1) if fence else raw

    m = re.search(r"\{.*\}", candidate, re.DOTALL)
    if not m:
        app.logger.error("No JSON object found in model response. Raw (first 2000 chars): %s", raw[:2000])
        return jsonify(error="Model returned an unparseable response, please retry."), 502
    json_text = m.group(0)
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        # Model occasionally emits a stray ';' where a ',' belongs (e.g. "...text";  ,)
        # or a trailing comma before a closing bracket. Try a light repair before giving up.
        repaired = re.sub(r'";(\s*),', r'",', json_text)
        repaired = re.sub(r',(\s*[}\]])', r'\1', repaired)
        try:
            data = json.loads(repaired)
        except json.JSONDecodeError as e:
            app.logger.error("JSON decode failed even after repair: %s. Raw (first 2000 chars): %s", e, raw[:2000])
            return jsonify(error="Model returned invalid JSON, please retry."), 502
    if data.get("error"):
        return jsonify(error=data["error"]), 422
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT, debug=False)
