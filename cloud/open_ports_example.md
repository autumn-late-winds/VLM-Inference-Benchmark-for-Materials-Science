# Ports And Security

- Backend dashboard API: `8000`
- Mock local multimodal server: `8001`
- vLLM cloud OpenAI-compatible server: `8001`
- Optional Transformers baseline: `8002`
- Optional GPU monitor: choose an internal port, then tunnel it

Recommended access pattern:

```bash
ssh -L 8001:localhost:8001 user@cloud-server
```

Avoid exposing unauthenticated model endpoints publicly. Put endpoints behind a firewall, private network, SSH tunnel, or authenticated reverse proxy.

