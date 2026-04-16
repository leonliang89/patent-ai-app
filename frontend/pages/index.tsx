import { useState } from "react";

const API = "https://patent-ai-app-production.up.railway.app";

export default function Home() {
  const [text, setText] = useState("");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generate = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError("");
    setData(null);
    try {
      const res = await fetch(`${API}/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const result = await res.json();
      setData(result);
    } catch (e: any) {
      setError(e.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const analysis = data?.analysis;

  return (
    <div style={{ padding: 40, maxWidth: 800, margin: "0 auto", fontFamily: "sans-serif" }}>
      <h1>AI Patent Generator</h1>

      <textarea
        style={{ width: "100%", height: 100, fontSize: 16, padding: 8 }}
        placeholder="Enter a technology keyword (e.g. AI sensor, autonomous vehicle...)"
        onChange={(e) => setText(e.target.value)}
        value={text}
      />

      <br /><br />

      <button
        onClick={generate}
        disabled={loading}
        style={{ padding: "8px 24px", fontSize: 16, cursor: loading ? "wait" : "pointer" }}
      >
        {loading ? "Searching USPTO..." : "Generate"}
      </button>

      {error && (
        <p style={{ color: "red", marginTop: 16 }}>⚠ {error}</p>
      )}

      {data && (
        <div>
          {/* ── Patent 區塊 ── */}
          <h2>Patent</h2>
          <pre style={{
            background: "#f5f5f5", padding: 16, borderRadius: 8,
            whiteSpace: "pre-wrap", wordBreak: "break-word", fontSize: 13
          }}>
            {data.patent}
          </pre>

          {/* ── Analysis 區塊 ── */}
          {analysis && (
            <>
              <h2>Analysis
                <span style={{ fontSize: 13, fontWeight: "normal", color: "#888", marginLeft: 8 }}>
                  {analysis.source}
                </span>
              </h2>

              <div style={{ display: "flex", gap: 24, flexWrap: "wrap", marginBottom: 16 }}>
                <div style={{ background: "#e8f4fd", borderRadius: 8, padding: "12px 24px" }}>
                  <div style={{ fontSize: 28, fontWeight: "bold" }}>{analysis.total_patents}</div>
                  <div style={{ color: "#555", fontSize: 13 }}>Patents Found</div>
                </div>
                <div style={{ background: "#f0fdf4", borderRadius: 8, padding: "12px 24px" }}>
                  <div style={{ fontSize: 14, fontWeight: "bold" }}>
                    {analysis.top_keywords?.join("  ·  ") || "—"}
                  </div>
                  <div style={{ color: "#555", fontSize: 13 }}>Top Keywords</div>
                </div>
              </div>

              {/* ── 近期專利列表 ── */}
              {analysis.recent_patents?.length > 0 && (
                <>
                  <h3 style={{ marginBottom: 8 }}>Recent Patents</h3>
                  <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
                    <thead>
                      <tr style={{ background: "#f0f0f0" }}>
                        <th style={th}>Patent ID</th>
                        <th style={th}>Title</th>
                        <th style={th}>Assignee</th>
                        <th style={th}>Date</th>
                      </tr>
                    </thead>
                    <tbody>
                      {analysis.recent_patents.map((p: any, i: number) => (
                        <tr key={i} style={{ borderBottom: "1px solid #eee" }}>
                          <td style={td}>
                            <a
                              href={`https://patents.google.com/patent/US${p.id}`}
                              target="_blank"
                              rel="noreferrer"
                              style={{ color: "#1a73e8" }}
                            >
                              US{p.id}
                            </a>
                          </td>
                          <td style={td}>{p.title}</td>
                          <td style={td}>{p.assignee}</td>
                          <td style={td}>{p.date}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </>
              )}

              {analysis.note && (
                <p style={{ color: "#e67e22", marginTop: 8 }}>ℹ {analysis.note}</p>
              )}
            </>
          )}

          {/* ── 圖表 ── */}
          <h2>Distribution Chart</h2>
          <img
            src={`${API}/chart?t=${Date.now()}`}
            width="100%"
            style={{ maxWidth: 600, borderRadius: 8 }}
            alt="Patent distribution chart"
          />
        </div>
      )}
    </div>
  );
}

const th: React.CSSProperties = {
  textAlign: "left", padding: "6px 10px", fontWeight: 600
};
const td: React.CSSProperties = {
  padding: "6px 10px", verticalAlign: "top"
};
