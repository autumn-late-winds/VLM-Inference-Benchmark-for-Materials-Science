export function ResultsTable({ runs, onSelect }: { runs: any[]; onSelect: (id: string) => void }) {
  return (
    <section className="panel">
      <h2>Benchmark Runs</h2>
      <table>
        <thead><tr><th>Run</th><th>Requests</th><th>Mean Latency</th><th>RPS</th><th>Quality</th></tr></thead>
        <tbody>
          {runs.map((run) => (
            <tr key={run.run_id} onClick={() => onSelect(run.run_id)}>
              <td>{run.run_id}</td>
              <td>{run.summary?.total_requests}</td>
              <td>{run.summary?.mean_latency_ms}</td>
              <td>{run.summary?.requests_per_second}</td>
              <td>{run.summary?.mean_keyword_coverage_score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

