import { Activity, BarChart3, Database, FileText, FlaskConical, Server, TestTube2 } from "lucide-react";
import { useEffect, useState } from "react";
import { BenchmarkConfig } from "./components/BenchmarkConfig";
import { CostPanel } from "./components/CostPanel";
import { DatasetPreview } from "./components/DatasetPreview";
import { DeploymentPanel } from "./components/DeploymentPanel";
import { ExampleViewer } from "./components/ExampleViewer";
import { ImagePlayground } from "./components/ImagePlayground";
import { LatencyChart } from "./components/LatencyChart";
import { QualityScorePanel } from "./components/QualityScorePanel";
import { ReportViewer } from "./components/ReportViewer";
import { ResultsTable } from "./components/ResultsTable";
import { ThroughputChart } from "./components/ThroughputChart";
import { apiGet } from "./api/client";

const tabs = [
  { id: "home", label: "Home", icon: Activity },
  { id: "deployments", label: "Deployments", icon: Server },
  { id: "dataset", label: "Dataset", icon: Database },
  { id: "playground", label: "Playground", icon: TestTube2 },
  { id: "benchmark", label: "Benchmark", icon: FlaskConical },
  { id: "results", label: "Results", icon: BarChart3 },
  { id: "report", label: "Report", icon: FileText },
];

export function App() {
  const [tab, setTab] = useState("home");
  const [runs, setRuns] = useState<any[]>([]);
  const [selectedRun, setSelectedRun] = useState<any | null>(null);

  async function refreshRuns() {
    const data = await apiGet<any[]>("/benchmark/runs").catch(() => []);
    setRuns(data);
    if (data.length && !selectedRun) {
      const latest = await apiGet<any>(`/benchmark/runs/${data[data.length - 1].run_id}`).catch(() => null);
      setSelectedRun(latest);
    }
  }

  useEffect(() => {
    refreshRuns();
  }, []);

  return (
    <main>
      <aside>
        <div className="brand">
          <span>Materials VLM</span>
          <strong>Inference Benchmark</strong>
        </div>
        <nav>
          {tabs.map((item) => {
            const Icon = item.icon;
            return (
              <button key={item.id} className={tab === item.id ? "active" : ""} onClick={() => setTab(item.id)}>
                <Icon size={18} />
                {item.label}
              </button>
            );
          })}
        </nav>
      </aside>
      <section className="page">
        {tab === "home" && <Home />}
        {tab === "deployments" && <DeploymentPanel />}
        {tab === "dataset" && <DatasetPreview />}
        {tab === "playground" && <ImagePlayground />}
        {tab === "benchmark" && <BenchmarkConfig onDone={refreshRuns} />}
        {tab === "results" && (
          <div className="stack">
            <ResultsTable runs={runs} onSelect={async (id) => setSelectedRun(await apiGet<any>(`/benchmark/runs/${id}`))} />
            <div className="grid two">
              <LatencyChart run={selectedRun} />
              <ThroughputChart runs={runs} />
              <CostPanel run={selectedRun} />
              <QualityScorePanel run={selectedRun} />
            </div>
            <ExampleViewer run={selectedRun} />
          </div>
        )}
        {tab === "report" && <ReportViewer runs={runs} />}
      </section>
    </main>
  );
}

function Home() {
  return (
    <div className="stack">
      <header className="hero">
        <p>Vision-language model serving and benchmarking for materials science inference workloads.</p>
        <h1>Materials VLM Inference Benchmark Dashboard</h1>
      </header>
      <div className="grid three">
        <article>
          <h2>Local Dashboard Mode</h2>
          <p>Frontend, backend, benchmark client, and mock multimodal server run locally. No Qwen3-VL weights are downloaded.</p>
        </article>
        <article>
          <h2>Remote API Mode</h2>
          <p>Connect to an OpenAI-compatible multimodal endpoint with configurable base URL, model, API key, timeout, and retry path.</p>
        </article>
        <article>
          <h2>Cloud GPU Mode</h2>
          <p>Qwen/Qwen3-VL-8B-Instruct is deployed only on a cloud GPU server through vLLM or the optional Transformers baseline.</p>
        </article>
      </div>
    </div>
  );
}

