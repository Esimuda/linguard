# Seed prompts

Multilingual red-team **research** prompts for Linguard.

| File | Language |
|------|----------|
| `en.jsonl` | English |
| `pcm.jsonl` | Nigerian Pidgin |
| `yo.jsonl` | Yoruba |
| `ha.jsonl` | Hausa |
| `ig.jsonl` | Igbo |

Schema per line:

```json
{
  "id": "pcm-scam-001",
  "language": "pcm",
  "category": "scam",
  "expected_behavior": "refuse",
  "tags": ["419"],
  "text": "..."
}
```

Categories: `scam`, `social_eng`, `harmful_advice`, `refusal_failure`, `benign`.

These prompts are for **AI safety evaluation only**. Do not use them to harm people.
