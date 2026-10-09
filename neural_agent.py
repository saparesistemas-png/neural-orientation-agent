#!/usr/bin/env python3
"""
Neural Orientation Agent
Engineer of attention and perceptual resolution.
Zero external dependencies beyond the Python standard library.
"""

from __future__ import annotations

import json
import urllib.request
import urllib.error
from typing import List, Dict

from neural_config import (
    SYSTEM_PROMPT,
    MAX_HISTORY_MESSAGES,
    EXIT_COMMANDS,
    AGENT_NAME,
    AGENT_TAGLINE,
    LLM_BASE_URL,
    LLM_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_TIMEOUT,
)


# ============================================================
# LLM CALL - OpenAI-compatible backend (stdlib only)
# ============================================================

def call_llm(messages: List[Dict[str, str]]) -> str:
    """
    Call any OpenAI-compatible chat completions endpoint.
    Uses only the Python standard library (urllib + json).
    """
    if not LLM_API_KEY:
        raise RuntimeError(
            "LLM_API_KEY not set. Export the environment variable before running:\n"
            "  export LLM_API_KEY='your-key-here'"
        )

    url = f"{LLM_BASE_URL.rstrip('/')}/chat/completions"

    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "temperature": LLM_TEMPERATURE,
        "stream": False,
    }

    data = json.dumps(payload).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LLM_API_KEY}",
    }

    request = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=LLM_TIMEOUT) as response:
            body = response.read().decode("utf-8")
            result = json.loads(body)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"LLM HTTP {e.code}: {error_body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"LLM connection error: {e.reason}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"LLM returned invalid JSON: {e}") from e

    try:
        return result["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"Unexpected LLM response format: {result}") from e


# ============================================================
# HISTORY MANAGEMENT
# ============================================================

def trim_history(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Keep the system message + the most recent messages
    within MAX_HISTORY_MESSAGES limit.
    """
    if len(messages) <= MAX_HISTORY_MESSAGES:
        return messages

    system = messages[0]
    recent = messages[-(MAX_HISTORY_MESSAGES - 1):]
    return [system] + recent


# ============================================================
# AGENT LOOP
# ============================================================

def run_agent() -> None:
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print("=" * 60)
    print(AGENT_NAME)
    print(AGENT_TAGLINE)
    print(f"Model: {LLM_MODEL}  |  Backend: {LLM_BASE_URL}")
    print(f"Type {', '.join(sorted(EXIT_COMMANDS))} to stop.")
    print("=" * 60)
    print()

    while True:
        try:
            user_input = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrado.")
            break

        if user_input.lower() in EXIT_COMMANDS:
            print("Agente finalizado.")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        messages = trim_history(messages)

        try:
            response = call_llm(messages)
        except Exception as e:
            print(f"\n[ERRO] {e}\n")
            messages.pop()  # remove the failed user message
            continue

        print(f"\nAgente: {response}\n")
        messages.append({"role": "assistant", "content": response})
        messages = trim_history(messages)


if __name__ == "__main__":
    run_agent()
