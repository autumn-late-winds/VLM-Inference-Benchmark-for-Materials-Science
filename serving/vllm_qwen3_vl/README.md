# vLLM Qwen3-VL Cloud Serving

This folder is cloud-only. Running the script can download `Qwen/Qwen3-VL-8B-Instruct` weights to the server cache.

Use SSH tunneling from your laptop:

```bash
ssh -L 8001:localhost:8001 user@cloud-server
```

Then point the dashboard to `http://localhost:8001/v1`.

Do not expose an unauthenticated OpenAI-compatible endpoint directly to the public internet.

