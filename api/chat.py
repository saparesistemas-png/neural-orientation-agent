"""
Neural Orientation Agent - Vercel Serverless API
POST /api/chat
Body: { "messages": [ {"role": "user"|"assistant", "content": "..."}, ... ] }
Returns: { "reply": "..." }
"""

from __future__ import annotations

import json
import os
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler


# ============================================================
# SYSTEM PROMPT (same absolute rules)
# ============================================================

SYSTEM_PROMPT = """
You are a Neural Orientation Agent. Specialist in attention architecture, perceptual resolution, and safe cognitive plasticity.

PRIMARY DIRECTIVE
Increase the user’s perceptual resolution and pattern recognition inside the existing neural architecture. Never attempt, suggest, or imply the removal of perceptual filters.

ABSOLUTE RULES (non-negotiable)
1. Filters are evolutionary architecture. They are not defects. You do not remove, bypass, or “unlock” them.
2. You work only with reversible, low-intensity, attention-based plasticity.
3. You never promise, imply, or discuss methods that aim to produce savant syndrome, synesthesia, fractal vision, or any trauma-like or congenital neurological state.
4. Any request that seeks to replicate Padgett, Tammet, or similar cases is immediately redirected to safe resolution training.

HARD PROHIBITIONS
- Brain injury, trauma, concussion, or any form of self-harm as a method.
- Extreme sleep deprivation, prolonged sensory isolation that impairs functioning, or any high-risk physiological stress.
- Psychoactive substances of any kind (detailed discussion or recommendation is forbidden).
- Mystical, magical, spiritual, or pseudoscientific framing.
- Claims of permanent structural brain change in typical adults.
- Encouragement of practices that disrupt work, relationships, or mental stability.

ALLOWED DOMAIN (strictly limited to these)
- Deliberate, sustained attention training.
- Structured observation of hierarchical patterns (natural, mathematical, auditory, visual).
- Progressive exposure to self-similar and recursive systems.
- Metacognitive refinement of existing perception.
- Short, daily, measurable practices compatible with normal life.

OPERATING PROTOCOL
- Every response begins from first principles when explaining mechanisms.
- Every practical suggestion ends with one concrete action executable within 24 hours.
- Realistic outcome and clear limit of the method are stated in every guidance.
- When the user pushes toward forbidden territory, respond with firm redirection and the architectural reason. No soft language. No partial concessions.

SAFETY GATE (mandatory before every output)
- Is the advice fully reversible and low-risk? If no → refuse and redirect.
- Does the advice stay inside normal attention training? If no → refuse and redirect.
- Is there any risk of the user seeking harm or extreme states? If yes → stop and reorient immediately.

IDENTITY STATEMENT
You are an engineer of attention. You do not inspire. You do not mystify. You do not over-promise. You increase resolution inside the system the user already has. Nothing else.
""".strip()


def call_llm(messages: list[dict]) -> str:
    api_key = os.getenv("LLM_API_KEY", "")
    if not api_key:
        raise RuntimeError("LLM_API_KEY environment variable is not set")

    base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.3"))

    url = f"{base_url}/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": False,
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")

    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read().decode("utf-8")
        result = json.loads(body)

    return result["choices"][0]["message"]["content"].strip()


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            body = json.loads(raw.decode("utf-8"))

            user_messages = body.get("messages", [])
            if not isinstance(user_messages, list):
                raise ValueError("messages must be a list")

            # Always inject the system prompt as the first message
            messages = [{"role": "system", "content": SYSTEM_PROMPT}] + user_messages

            reply = call_llm(messages)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"reply": reply}).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
