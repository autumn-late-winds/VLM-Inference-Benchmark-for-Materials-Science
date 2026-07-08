import { useEffect, useState } from "react";
import { apiGet, apiPost } from "../api/client";

export function DeploymentPanel() {
  const [deployments, setDeployments] = useState<any[]>([]);
  const [form, setForm] = useState({
    deployment_id: "remote_api",
    name: "Remote OpenAI-Compatible API",
    backend_type: "external_openai_compatible",
    base_url: "http://localhost:8001/v1",
    api_key: "EMPTY",
    model_name: "Qwen/Qwen3-VL-8B-Instruct",
    notes: "",
  });
  const [status, setStatus] = useState("");

  async function load() {
    setDeployments(await apiGet<any[]>("/deployments"));
  }
  useEffect(() => {
    load();
  }, []);

  async function register() {
    await apiPost("/deployments/register", form);
    await load();
  }

  async function test() {
    setStatus("Testing...");
    const res = await apiPost<any>("/deployments/test", form).catch((e) => ({ ok: false, response: e.message }));
    setStatus(JSON.stringify(res, null, 2));
  }

  return (
    <div className="stack">
      <h1>Deployments</h1>
      <div className="grid two">
        <section className="panel">
          <h2>Register Endpoint</h2>
          {Object.entries(form).map(([key, value]) => (
            <label key={key}>
              {key}
              <input value={value} onChange={(e) => setForm({ ...form, [key]: e.target.value })} />
            </label>
          ))}
          <div className="actions">
            <button onClick={register}>Register</button>
            <button onClick={test}>Test</button>
          </div>
          <pre>{status}</pre>
        </section>
        <section className="panel">
          <h2>Known Endpoints</h2>
          <div className="list">
            {deployments.map((item) => (
              <article key={item.deployment_id}>
                <strong>{item.name}</strong>
                <span>{item.backend_type}</span>
                <code>{item.base_url}</code>
                <small>{item.model_name}</small>
              </article>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

