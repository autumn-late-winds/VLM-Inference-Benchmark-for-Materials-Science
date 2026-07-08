export function QualityScorePanel({ run }: { run: any | null }) {
  return <section className="panel"><h2>Quality</h2><p className="big">{run?.summary?.mean_keyword_coverage_score ?? "No run selected"}</p><small>Approximate keyword coverage, dataset dependent.</small></section>;
}

