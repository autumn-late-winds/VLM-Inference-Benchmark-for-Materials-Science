# Materials VLM Inference Benchmark Dashboard

An MVP dashboard for benchmarking OpenAI-compatible multimodal model serving on materials science image-text workloads. It supports local mock mode, remote multimodal API mode, and cloud GPU Qwen3-VL deployment mode.

The local default is deliberately safe: it does not download Qwen3-VL weights. Local development runs the React dashboard, FastAPI backend, benchmark client, and mock multimodal server only.

## Architecture

```text
React/Vite dashboard
  -> FastAPI backend control API
     -> OpenAI-compatible multimodal client
        -> local mock server, remote API, or cloud vLLM Qwen3-VL endpoint
     -> benchmark runner
     -> JSON/CSV result store and Markdown/JSON reports
```

## What Works In This MVP

- Deployment registry and endpoint test.
- Synthetic materials demo dataset generation.
- Dataset validation, stats, and preview.
- OpenAI-compatible multimodal request construction with base64 image payloads.
- Local mock `/v1/chat/completions` server.
- Single-image, multi-image, and text-only benchmark execution.
- Latency, throughput, cost estimate, and keyword coverage metrics.
- JSON, CSV, Markdown report generation.
- Dashboard pages for deployments, dataset preview, playground, benchmark, results, qualitative examples, and reports.
- Cloud-only vLLM Qwen3-VL deployment scripts.
- Protected Transformers baseline stub that refuses to run unless `ALLOW_LOCAL_MODEL_DOWNLOAD=true`.

## No Local Qwen3-VL Downloads

The project defaults are:

```env
LOCAL_MOCK_MODE=true
ALLOW_LOCAL_MODEL_DOWNLOAD=false
OPENAI_COMPATIBLE_BASE_URL=http://localhost:8001/v1
```

There is no local `from_pretrained("Qwen/Qwen3-VL-8B-Instruct")` path in the dashboard, backend, benchmark runner, or mock server. The optional Transformers baseline is cloud-only and returns HTTP 403 unless `ALLOW_LOCAL_MODEL_DOWNLOAD=true`.

## Local Mock Mode

From this project folder:

```bash
python benchmark/scripts/build_demo_dataset.py
docker compose -f docker-compose.local.yml up --build
```

Open:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Mock multimodal endpoint: `http://localhost:8001/v1`

This mode uses deterministic mock responses and downloads no model weights.

## Run Without Docker

Terminal 1:

```bash
cd serving/mock_multimodal_server
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8001
```

Terminal 2:

```bash
pip install -r backend/requirements.txt
python benchmark/scripts/build_demo_dataset.py
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
```

Terminal 3:

```bash
cd frontend
npm install
npm run dev
```

## External OpenAI-Compatible API Mode

Set:

```env
OPENAI_COMPATIBLE_BASE_URL=https://your-provider.example/v1
OPENAI_COMPATIBLE_API_KEY=your_key
DEFAULT_MODEL=your-multimodal-model
LOCAL_MOCK_MODE=false
ALLOW_LOCAL_MODEL_DOWNLOAD=false
```

Then register the endpoint in the Deployments page or edit `results/deployments.json`.

Expected request shape:

```json
{
  "model": "Qwen/Qwen3-VL-8B-Instruct",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What morphology is shown in this SEM image?"},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
      ]
    }
  ],
  "max_tokens": 256,
  "temperature": 0
}
```

## Cloud Qwen3-VL With vLLM

On the cloud GPU server:

```bash
cd cloud
bash check_gpu_env.sh
bash setup_cloud_gpu_server.sh
MODEL_NAME=Qwen/Qwen3-VL-8B-Instruct PORT=8001 bash deploy_vllm_qwen3_vl.sh
```

From your laptop:

```bash
ssh -L 8001:localhost:8001 user@cloud-server
```

Then point the dashboard to:

```text
http://localhost:8001/v1
```

vLLM support for Qwen3-VL depends on the installed vLLM version and model compatibility. Keep the endpoint private, behind SSH tunneling, firewall rules, or authenticated reverse proxy.

## Benchmark Commands

Generate the demo dataset:

```bash
python benchmark/scripts/build_demo_dataset.py
```

Run a small benchmark against the mock or tunneled endpoint:

```bash
python benchmark/scripts/run_benchmark.py --config benchmark/configs/benchmark_small.yaml
```

Run a matrix:

```bash
python benchmark/scripts/run_benchmark_matrix.py --config benchmark/configs/benchmark_concurrency.yaml
```

Summarize saved results:

```bash
python benchmark/scripts/summarize_results.py
```

## Metrics

Per request:

- latency, success/failure, task type, modality, input mode, image count, total pixels
- token usage when available
- model response and reference answer
- keyword coverage and quality notes

Per run:

- mean, median, P50, P90, P95, P99 latency
- requests per second
- mean keyword coverage
- GPU metrics when configured
- estimated cost per run, 1k requests, 1M output tokens, and image-text request

Cost numbers are estimates based on user-provided GPU hourly price.

## Quality Interpretation

Keyword coverage is a lightweight engineering signal. It is not equivalent to scientific correctness. Synthetic demo images are only for validating the serving, benchmark, and dashboard workflow.

Real scientific evaluation requires expert-curated datasets, task-specific rubrics, and human review. VLM outputs may hallucinate peaks, materials, and performance values.

## Security Notes

- Never hard-code API keys.
- Prefer SSH tunneling: `ssh -L 8001:localhost:8001 user@cloud-server`.
- Do not expose unauthenticated model endpoints publicly.
- Use firewall rules, private networking, or authenticated reverse proxy for cloud deployments.

## Tests

```bash
pip install -r backend/requirements.txt
PYTHONPATH=backend pytest backend/tests
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH="backend"
pytest backend/tests
```

## Future Improvements

- Real materials figure dataset.
- OCR-enhanced plot understanding.
- Figure panel detection.
- Larger multimodal benchmark set.
- Comparison across Qwen3-VL, InternVL, LLaVA, and GPT-style APIs.
- Prometheus and Grafana monitoring.
- Kubernetes deployment.
- Integration with a Materials Multimodal RAG Assistant.

## Phase Status

- Phase 1: skeleton, backend API, frontend dashboard, mock server, Docker local mode, demo generator, README are implemented.
- Phase 2: dataset validation, stats, preview, and upload endpoint are implemented; full image bundle upload remains a TODO.
- Phase 3: OpenAI-compatible multimodal client and inference playground are implemented.
- Phase 4: benchmark runner, metric calculation, result storage, and report generation are implemented.
- Phase 5: dashboard visualizations are implemented at MVP level.
- Phase 6: cloud vLLM deployment scripts are implemented.
- Phase 7: protected Transformers baseline stub is implemented; full model server remains cloud-only TODO.
- Phase 8: initial tests are implemented; broader integration tests remain TODO.

