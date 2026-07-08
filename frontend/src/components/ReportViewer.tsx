import { useState } from "react";
import { apiGet } from "../api/client";

export function ReportViewer({ runs }: { runs: any[] }) {
  const [text, setText] = useState("");
  async function load(id: string) {
    setText(await apiGet<string>(`/reports/${id}/markdown`));
  }
  return <div className="stack"><h1>Report</h1><section className="panel"><div className="actions">{runs.map((r) => <button key={r.run_id} onClick={() => load(r.run_id)}>{r.run_id.slice(-8)}</button>)}</div><pre>{text}</pre></section></div>;
}

