export function ExampleViewer({ run }: { run: any | null }) {
  const examples = run?.results?.slice(0, 4) || [];
  return <section className="panel"><h2>Qualitative Examples</h2><div className="list">{examples.map((item: any) => <article key={item.request_id}><strong>{item.modality} · {item.task_type}</strong><p>{item.model_response}</p><small>Reference: {item.reference_answer}</small><code>score {item.keyword_coverage_score}</code></article>)}</div></section>;
}

