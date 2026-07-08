import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export function LatencyChart({ run }: { run: any | null }) {
  const data = run ? [{ name: "mean", value: run.summary.mean_latency_ms }, { name: "p95", value: run.summary.p95_latency_ms }, { name: "p99", value: run.summary.p99_latency_ms }] : [];
  return <section className="panel"><h2>Latency</h2><ResponsiveContainer height={240}><BarChart data={data}><CartesianGrid /><XAxis dataKey="name" /><YAxis /><Tooltip /><Bar dataKey="value" fill="#2563eb" /></BarChart></ResponsiveContainer></section>;
}

