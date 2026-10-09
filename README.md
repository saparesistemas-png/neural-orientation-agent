# Neural Orientation Agent

Engineer of attention — resolution inside existing architecture.

Safe cognitive plasticity training. No filter removal. No savant promises. No mysticism.

## Core Principle

Filters are evolutionary architecture.  
The agent increases perceptual resolution **inside** the architecture the user already has.

## Files

| File | Purpose |
|------|---------|
| `neural_config.py` | Absolute system prompt + runtime parameters |
| `neural_agent.py` | CLI interactive agent (terminal) |
| `api/chat.py` | Vercel Serverless API endpoint |

## CLI Usage

```bash
export LLM_API_KEY="your-key"
export LLM_BASE_URL="https://api.openai.com/v1"   # optional
export LLM_MODEL="gpt-4o-mini"                    # optional

python neural_agent.py
```

Compatible with any OpenAI-compatible endpoint (OpenAI, Groq, Together, Ollama, LM Studio…).

## Vercel API Usage

1. Import the repository into Vercel (or connect the GitHub repo).
2. Set environment variables in the Vercel project:
   - `LLM_API_KEY` (required)
   - `LLM_BASE_URL` (optional)
   - `LLM_MODEL` (optional)
3. Deploy.

### Endpoint

```
POST /api/chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Como treinar atenção visual?"}
  ]
}
```

Response:

```json
{
  "reply": "..."
}
```

## Absolute Rules (never diluted)

- Filters are not defects.
- Only reversible, low-intensity attention training.
- No trauma, no substances, no extreme deprivation.
- No promises of savant syndrome or synesthesia.
- Firm redirection when the user asks for the impossible.

## License

Use freely. Keep the safety rules intact.
