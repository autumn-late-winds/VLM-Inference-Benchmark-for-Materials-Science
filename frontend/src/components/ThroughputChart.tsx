import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export function ThroughputChart({ runs }: { runs: any[] }) {
  const data = runs.map((r) => ({ name: r.run_id.slice(-6), rps: r.summary?.requests_per_second || 0 }));
  return <section className="panel"><h2>Throughput</h2><ResponsiveContainer height={240}><LineChart data={data}><XAxis dataKey="name" /><YAxis /><Tooltip /><Line dataKey="rps" stroke="#16a34a" strokeWidth={2} /></LineChart></ResponsiveContainer></section>;
}

