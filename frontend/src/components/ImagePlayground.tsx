import { useState } from "react";
import { apiPost } from "../api/client";

export function ImagePlayground() {
  const [question, setQuestion] = useState("What morphology is shown in this SEM image?");
  const [imagePath, setImagePath] = useState("data/demo/images/sem_001.png");
  const [response, setResponse] = useState<any | null>(null);
  async function run() {
    setResponse(await apiPost("/inference/query", { question, image_paths: imagePath ? [imagePath] : [] }));
  }
  return (
    <div className="stack">
      <h1>Playground</h1>
      <section className="panel">
        <label>Image path<input value={imagePath} onChange={(e) => setImagePath(e.target.value)} /></label>
        <label>Question<textarea value={question} onChange={(e) => setQuestion(e.target.value)} /></label>
        <button onClick={run}>Run Inference</button>
      </section>
      <section className="panel">
        <h2>Response</h2>
        <pre>{JSON.stringify(response, null, 2)}</pre>
      </section>
    </div>
  );
}

