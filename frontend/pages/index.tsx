import { useState } from "react";

export default function Home() {
  const [text, setText] = useState("");
  const [data, setData] = useState(null);

  const generate = async () => {
  const generate = async () => {
  const res = await fetch("https://patent-ai-app-production.up.railway.app/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text })
  });

  const result = await res.json();
  setData(result);
};

  return (
    <div style={{ padding: 40 }}>
      <h1>AI Patent Generator</h1>

      <textarea onChange={(e) => setText(e.target.value)} />

      <button onClick={generate}>Generate</button>

      {data && (
        <div>
          <h2>Patent</h2>
          <pre>{data.patent}</pre>

          <h2>Analysis</h2>
          <pre>{JSON.stringify(data.analysis, null, 2)}</pre>

          <img src="https://patent-ai-app-production.up.railway.app/chart" />
        </div>
      )}
    </div>
  );
}
