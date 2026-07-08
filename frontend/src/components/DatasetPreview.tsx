import { useEffect, useState } from "react";
import { API_BASE, apiGet } from "../api/client";

export function DatasetPreview() {
  const [examples, setExamples] = useState<any[]>([]);
  const [stats, setStats] = useState<any | null>(null);
  useEffect(() => {
    apiGet<any>("/datasets/synthetic_demo").then((d) => setStats(d.stats)).catch(() => null);
    apiGet<any[]>("/datasets/synthetic_demo/examples?limit=12").then(setExamples).catch(() => []);
  }, []);
  return (
    <div className="stack">
      <h1>Dataset</h1>
      <section className="panel">
        <h2>Synthetic Demo Statistics</h2>
        <pre>{JSON.stringify(stats, null, 2)}</pre>
      </section>
      <div className="grid three">
        {examples.map((item) => (
          <article key={item.id}>
            <img src={`${API_BASE}/${item.image_paths[0]}`} />
            <strong>{item.modality}</strong>
            <p>{item.question}</p>
            <small>{item.expected_keywords.join(", ")}</small>
          </article>
        ))}
      </div>
    </div>
  );
}
