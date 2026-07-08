import { useState } from "react";
import { apiPost } from "../api/client";

export function BenchmarkConfig({ onDone }: { onDone: () => void }) {
  const [config, setConfig] = useState({
    run_name: "dashboard_local_smoke",
    deployment_id: "local_mock",
    dataset_file: "data/demo/materials_vlm_demo.jsonl",
    image_root: ".",
    input_mode: "single_image",
    image_resolution: "512",
    number_of_images: 1,
    concurrency: 1,
    max_output_tokens: 128,
    num_warmup_requests: 1,
    num_measured_requests: 5,
    stream: false,
    timeout_seconds: 60,
    temperature: 0,
    save_model_responses: true,
    cost_per_gpu_hour_usd: 1.5,
  });
  const [result, setResult] = useState<any | null>(null);
  async function run() {
    const data = await apiPost<any>("/benchmark/run", config);
    setResult(data);
    onDone();
  }
  return (
    <div className="stack">
      <h1>Benchmark</h1>
      <section className="panel form-grid">
        {Object.entries(config).map(([key, value]) => (
          <label key={key}>
            {key}
            <input
              value={String(value)}
              onChange={(e) => setConfig({ ...config, [key]: Number.isFinite(Number(value)) ? Number(e.target.value) : e.target.value })}
            />
          </label>
        ))}
        <button onClick={run}>Start Benchmark</button>
      </section>
      <section className="panel">
        <h2>Progress And Summary</h2>
        <pre>{JSON.stringify(result?.summary ?? result, null, 2)}</pre>
      </section>
    </div>
  );
}

