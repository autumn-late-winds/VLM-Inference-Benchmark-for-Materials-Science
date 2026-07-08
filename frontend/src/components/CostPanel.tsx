export function CostPanel({ run }: { run: any | null }) {
  return <section className="panel"><h2>Cost</h2><pre>{JSON.stringify(run?.summary ? {
    cost_per_1k_requests: run.summary.estimated_cost_per_1k_requests,
    cost_per_1M_output_tokens: run.summary.estimated_cost_per_1M_output_tokens,
    cost_per_image_text_request: run.summary.estimated_cost_per_image_text_request,
  } : {}, null, 2)}</pre></section>;
}

