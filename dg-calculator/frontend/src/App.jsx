import { useState } from "react";
import axios from "axios";

const API = "http://localhost:8000";

const defaultInputs = {
  daily_consumption_kwh: "",
  peak_sun_hours: "",
  system_efficiency: 0.8,
  safety_margin: 1.1,
  panel_wattage: 400,
};

export default function App() {
  const [tab, setTab] = useState("calculator");
  const [inputs, setInputs] = useState(defaultInputs);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [messages, setMessages] = useState([
    { role: "agent", text: "Hi! Describe your energy needs and I'll calculate the solar system size you need. For example: \"I need solar panels for a house that uses 30 kWh a day in Mumbai\"" }
  ]);
  const [userInput, setUserInput] = useState("");
  const [agentLoading, setAgentLoading] = useState(false);

  function handleChange(e) {
    setInputs({ ...inputs, [e.target.name]: parseFloat(e.target.value) || e.target.value });
  }

  async function handleCalculate() {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await axios.post(`${API}/calculate`, inputs);
      setResult(res.data);
    } catch {
      setError("Something went wrong. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  async function handleAgentSend() {
    if (!userInput.trim()) return;
    const userMsg = userInput.trim();
    setUserInput("");
    setMessages(prev => [...prev, { role: "user", text: userMsg }]);
    setAgentLoading(true);
    try {
      const res = await axios.post(`${API}/agent`, { message: userMsg });
      setMessages(prev => [...prev, { role: "agent", text: res.data.reply }]);
      if (res.data.data) {
        setMessages(prev => [...prev, { role: "result", data: res.data.data }]);
      }
    } catch {
      setMessages(prev => [...prev, { role: "agent", text: "Sorry, I couldn't process that. Please try again." }]);
    } finally {
      setAgentLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleAgentSend();
    }
  }

  return (
    <div style={styles.page}>
      {/* Header */}
      <div style={styles.header}>
        <div style={styles.headerInner}>
          <span style={styles.logo}>☀️</span>
          <div>
            <div style={styles.headerTitle}>DG Size Calculator</div>
            <div style={styles.headerSub}>Solar panel system sizing tool · Powered by AI</div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={styles.tabBar}>
        <button
          style={{ ...styles.tab, ...(tab === "calculator" ? styles.tabActive : {}) }}
          onClick={() => setTab("calculator")}
        >
          🧮 Calculator
        </button>
        <button
          style={{ ...styles.tab, ...(tab === "agent" ? styles.tabActive : {}) }}
          onClick={() => setTab("agent")}
        >
          🤖 AI Assistant
        </button>
      </div>

      {/* Content */}
      <div style={styles.content}>

        {/* Calculator Tab */}
        {tab === "calculator" && (
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>Enter Your Details</h2>
            <p style={styles.cardSub}>Fill in your energy consumption and location details below.</p>

            <div style={styles.form}>
              <Field label="Daily Energy Consumption (kWh)" name="daily_consumption_kwh"
                value={inputs.daily_consumption_kwh} onChange={handleChange} placeholder="e.g. 20" />
              <Field label="Peak Sun Hours" name="peak_sun_hours"
                value={inputs.peak_sun_hours} onChange={handleChange} placeholder="e.g. 5 for Mumbai" />

              <div style={styles.grid2}>
                <Field label="System Efficiency (0–1)" name="system_efficiency"
                  value={inputs.system_efficiency} onChange={handleChange} placeholder="e.g. 0.8" />
                <Field label="Safety Margin" name="safety_margin"
                  value={inputs.safety_margin} onChange={handleChange} placeholder="e.g. 1.1" />
              </div>

              <Field label="Panel Wattage (W)" name="panel_wattage"
                value={inputs.panel_wattage} onChange={handleChange} placeholder="e.g. 400" />
            </div>

            <button style={styles.button} onClick={handleCalculate} disabled={loading}>
              {loading ? "Calculating..." : "Calculate System Size"}
            </button>

            {error && <p style={styles.error}>{error}</p>}

            {result && (
              <div style={styles.results}>
                <h3 style={styles.resultsTitle}>Results</h3>
                <div style={styles.resultHighlights}>
                  <HighlightCard icon="⚡" label="System Size" value={`${result.dg_size_kw} kW`} />
                  <HighlightCard icon="🔲" label="Panels Needed" value={`${result.panel_count} panels`} />
                </div>
                <div style={styles.resultRows}>
                  <ResultRow label="Daily Generation" value={`${result.daily_generation_kwh} kWh`} />
                  <ResultRow label="Monthly Generation" value={`${result.monthly_generation_kwh} kWh`} />
                  <ResultRow label="Annual Generation" value={`${result.annual_generation_kwh} kWh`} />
                </div>
              </div>
            )}
          </div>
        )}

        {/* Agent Tab */}
        {tab === "agent" && (
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>AI Assistant</h2>
            <p style={styles.cardSub}>Describe your needs in plain English — the AI will calculate for you.</p>

            <div style={styles.chatBox}>
              {messages.map((msg, i) => (
                <div key={i}>
                  {msg.role === "result" ? (
                    <div style={styles.agentResultCard}>
                      <div style={styles.agentResultGrid}>
                        <AgentResultItem label="System Size" value={`${msg.data.dg_size_kw} kW`} />
                        <AgentResultItem label="Panels" value={`${msg.data.panel_count}`} />
                        <AgentResultItem label="Daily" value={`${msg.data.daily_generation_kwh} kWh`} />
                        <AgentResultItem label="Monthly" value={`${msg.data.monthly_generation_kwh} kWh`} />
                      </div>
                    </div>
                  ) : (
                    <div style={{
                      ...styles.bubble,
                      ...(msg.role === "user" ? styles.bubbleUser : styles.bubbleAgent)
                    }}>
                      {msg.text}
                    </div>
                  )}
                </div>
              ))}
              {agentLoading && (
                <div style={{ ...styles.bubble, ...styles.bubbleAgent }}>
                  Thinking...
                </div>
              )}
            </div>

            <div style={styles.chatInput}>
              <input
                style={styles.chatTextInput}
                placeholder="e.g. I need solar panels for a 30 kWh/day house in Delhi..."
                value={userInput}
                onChange={e => setUserInput(e.target.value)}
                onKeyDown={handleKeyDown}
              />
              <button style={styles.sendButton} onClick={handleAgentSend} disabled={agentLoading}>
                Send
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div style={styles.footer}>
        Built with FastAPI · MCP · React · MongoDB · Gemini AI &nbsp;·&nbsp; Actoryx Internship
      </div>
    </div>
  );
}

function Field({ label, name, value, onChange, placeholder }) {
  return (
    <div style={styles.field}>
      <label style={styles.label}>{label}</label>
      <input style={styles.input} type="number" name={name}
        value={value} onChange={onChange} placeholder={placeholder} />
    </div>
  );
}

function HighlightCard({ icon, label, value }) {
  return (
    <div style={styles.highlightCard}>
      <div style={styles.highlightIcon}>{icon}</div>
      <div style={styles.highlightValue}>{value}</div>
      <div style={styles.highlightLabel}>{label}</div>
    </div>
  );
}

function ResultRow({ label, value }) {
  return (
    <div style={styles.resultRow}>
      <span style={styles.resultLabel}>{label}</span>
      <span style={styles.resultValue}>{value}</span>
    </div>
  );
}

function AgentResultItem({ label, value }) {
  return (
    <div style={styles.agentResultItem}>
      <div style={styles.agentResultValue}>{value}</div>
      <div style={styles.agentResultLabel}>{label}</div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "linear-gradient(160deg, #0f172a 0%, #1e293b 100%)",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    color: "#f1f5f9",
  },
  header: {
    background: "rgba(255,255,255,0.05)",
    borderBottom: "1px solid rgba(255,255,255,0.08)",
    padding: "20px 24px",
  },
  headerInner: { maxWidth: "720px", margin: "0 auto", display: "flex", alignItems: "center", gap: "14px" },
  logo: { fontSize: "32px" },
  headerTitle: { fontSize: "20px", fontWeight: "700", color: "#f8fafc" },
  headerSub: { fontSize: "13px", color: "#94a3b8", marginTop: "2px" },
  tabBar: {
    maxWidth: "720px", margin: "0 auto", padding: "20px 24px 0",
    display: "flex", gap: "8px",
  },
  tab: {
    padding: "10px 20px", borderRadius: "8px", border: "1px solid rgba(255,255,255,0.1)",
    background: "transparent", color: "#94a3b8", cursor: "pointer", fontSize: "14px", fontWeight: "500",
  },
  tabActive: {
    background: "#f59e0b", color: "#0f172a", border: "1px solid #f59e0b", fontWeight: "700",
  },
  content: { maxWidth: "720px", margin: "0 auto", padding: "20px 24px 40px" },
  card: {
    background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: "16px", padding: "32px",
  },
  cardTitle: { fontSize: "20px", fontWeight: "700", marginBottom: "6px", color: "#f8fafc" },
  cardSub: { fontSize: "14px", color: "#94a3b8", marginBottom: "24px" },
  form: { display: "flex", flexDirection: "column", gap: "16px" },
  grid2: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" },
  field: { display: "flex", flexDirection: "column", gap: "6px" },
  label: { fontSize: "13px", fontWeight: "600", color: "#cbd5e1" },
  input: {
    padding: "11px 14px", borderRadius: "8px",
    border: "1px solid rgba(255,255,255,0.12)",
    background: "rgba(255,255,255,0.06)", color: "#f1f5f9",
    fontSize: "15px", outline: "none",
  },
  button: {
    marginTop: "24px", width: "100%", padding: "14px",
    background: "#f59e0b", color: "#0f172a", border: "none",
    borderRadius: "8px", fontSize: "16px", fontWeight: "700", cursor: "pointer",
  },
  error: { color: "#f87171", marginTop: "12px", fontSize: "14px" },
  results: { marginTop: "28px", borderTop: "1px solid rgba(255,255,255,0.08)", paddingTop: "24px" },
  resultsTitle: { fontSize: "16px", fontWeight: "700", marginBottom: "16px", color: "#f8fafc" },
  resultHighlights: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px", marginBottom: "16px" },
  highlightCard: {
    background: "rgba(245,158,11,0.1)", border: "1px solid rgba(245,158,11,0.3)",
    borderRadius: "12px", padding: "16px", textAlign: "center",
  },
  highlightIcon: { fontSize: "24px", marginBottom: "8px" },
  highlightValue: { fontSize: "22px", fontWeight: "700", color: "#f59e0b" },
  highlightLabel: { fontSize: "12px", color: "#94a3b8", marginTop: "4px" },
  resultRows: { display: "flex", flexDirection: "column", gap: "8px" },
  resultRow: {
    display: "flex", justifyContent: "space-between", padding: "10px 14px",
    borderRadius: "8px", background: "rgba(255,255,255,0.04)",
  },
  resultLabel: { color: "#94a3b8", fontSize: "14px" },
  resultValue: { fontWeight: "600", color: "#f1f5f9", fontSize: "14px" },
  chatBox: {
    minHeight: "320px", maxHeight: "400px", overflowY: "auto",
    display: "flex", flexDirection: "column", gap: "12px",
    marginBottom: "16px", padding: "4px",
  },
  bubble: {
    maxWidth: "85%", padding: "12px 16px", borderRadius: "12px",
    fontSize: "14px", lineHeight: "1.6",
  },
  bubbleAgent: {
    background: "rgba(255,255,255,0.06)", color: "#e2e8f0",
    alignSelf: "flex-start", borderBottomLeftRadius: "4px",
  },
  bubbleUser: {
    background: "#f59e0b", color: "#0f172a", fontWeight: "500",
    alignSelf: "flex-end", borderBottomRightRadius: "4px",
  },
  agentResultCard: {
    background: "rgba(245,158,11,0.08)", border: "1px solid rgba(245,158,11,0.2)",
    borderRadius: "12px", padding: "16px", alignSelf: "flex-start", width: "100%",
  },
  agentResultGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" },
  agentResultItem: { textAlign: "center" },
  agentResultValue: { fontSize: "18px", fontWeight: "700", color: "#f59e0b" },
  agentResultLabel: { fontSize: "12px", color: "#94a3b8", marginTop: "2px" },
  chatInput: { display: "flex", gap: "8px" },
  chatTextInput: {
    flex: 1, padding: "12px 14px", borderRadius: "8px",
    border: "1px solid rgba(255,255,255,0.12)",
    background: "rgba(255,255,255,0.06)", color: "#f1f5f9",
    fontSize: "14px", outline: "none",
  },
  sendButton: {
    padding: "12px 20px", background: "#f59e0b", color: "#0f172a",
    border: "none", borderRadius: "8px", fontWeight: "700",
    cursor: "pointer", fontSize: "14px",
  },
  footer: {
    textAlign: "center", padding: "24px", color: "#475569",
    fontSize: "12px", borderTop: "1px solid rgba(255,255,255,0.05)",
  },
};