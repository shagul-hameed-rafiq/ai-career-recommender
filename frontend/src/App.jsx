import React, { useState } from "react";

export default function App() {
  const [skills, setSkills] = useState("");
  const [interests, setInterests] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setResult(null);

    if (!skills.trim()) {
      setError("Please enter at least one skill.");
      return;
    }

    setLoading(true);
    try {
      const resp = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ skills, interests }),
      });

      if (!resp.ok) {
        throw new Error(`Server responded ${resp.status}`);
      }

      const json = await resp.json();
      setResult(json);
    } catch (err) {
      setError(
        "Failed to contact backend. Make sure Flask server is running. (" +
          err.message +
          ")"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        maxWidth: 720,
        margin: "36px auto",
        fontFamily: "Segoe UI, Roboto, Arial",
      }}
    >
      <h1 style={{ fontSize: 28, marginBottom: 8 }}>
        AI Career Recommender — Demo
      </h1>
      <p style={{ marginTop: 0, color: "#555" }}>
        Enter skills and interests (comma separated). This demo posts data to
        your Flask backend.
      </p>

      <form onSubmit={handleSubmit} style={{ marginTop: 16 }}>
        <label style={{ display: "block", marginBottom: 6 }}>Skills</label>
        <input
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          placeholder="e.g. Python, SQL, Machine Learning"
          style={{
            width: "100%",
            padding: "10px 12px",
            fontSize: 14,
            marginBottom: 12,
          }}
        />

        <label style={{ display: "block", marginBottom: 6 }}>Interests</label>
        <input
          value={interests}
          onChange={(e) => setInterests(e.target.value)}
          placeholder="e.g. Data Science, Web Development"
          style={{
            width: "100%",
            padding: "10px 12px",
            fontSize: 14,
            marginBottom: 12,
          }}
        />

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "10px 16px",
            borderRadius: 6,
            border: "1px solid #000",
            cursor: "pointer",
            backgroundColor: "#ffffff",
            color: "#000000",
            fontWeight: 600,
            transition: "all 0.2s ease-in-out",
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = "#f0f0f0")}
          onMouseOut={(e) => (e.target.style.backgroundColor = "#ffffff")}
        >
          {loading ? "Searching..." : "Search Careers"}
        </button>
      </form>

      {error && <div style={{ marginTop: 12, color: "crimson" }}>{error}</div>}

      {result && (
        <div
          style={{
            backgroundColor: "#1e1e1e",
            color: "#d4d4d4",
            padding: "16px 20px",
            borderRadius: "8px",
            fontSize: "15px",
            fontFamily: "Segoe UI, Roboto, Arial, sans-serif",
            border: "1px solid #333",
            marginTop: "10px",
          }}
        >
          {/* Main predicted career */}
          {result.career ? (
            <div style={{ textAlign: "center", marginBottom: 12 }}>
              <div style={{ fontSize: 14, color: "#9aa4ad" }}>
                Predicted Career
              </div>
              <div style={{ fontSize: 20, color: "#00ff99", fontWeight: 700 }}>
                {result.career}
              </div>
            </div>
          ) : (
            <div
              style={{
                textAlign: "center",
                marginBottom: 12,
                color: "#cfcfcf",
              }}
            >
              No prediction yet.
            </div>
          )}

          {/* Top-3 list */}
          {Array.isArray(result.top3) && result.top3.length > 0 && (
            <div>
              <div style={{ fontSize: 13, color: "#9aa4ad", marginBottom: 8 }}>
                Top 3 Matches
              </div>
              <ol style={{ marginTop: 0, paddingLeft: 18 }}>
                {result.top3.map((item, i) => {
                  const conf =
                    result.confidences && result.confidences[i]
                      ? (result.confidences[i] * 100).toFixed(0)
                      : null;
                  return (
                    <li key={i} style={{ marginBottom: 8, color: "#e6eef1" }}>
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                        }}
                      >
                        <span>{item}</span>
                        {conf !== null && (
                          <span style={{ fontSize: 13, color: "#9aa4ad" }}>
                            {conf}%
                          </span>
                        )}
                      </div>
                      {/* small progress bar */}
                      {conf !== null && (
                        <div
                          style={{
                            height: 6,
                            width: "100%",
                            background: "#111",
                            borderRadius: 6,
                            marginTop: 6,
                            overflow: "hidden",
                          }}
                        >
                          <div
                            style={{
                              height: "100%",
                              width: `${conf}%`,
                              background: "#00b37e",
                              borderRadius: 6,
                              transition: "width 300ms ease",
                            }}
                          />
                        </div>
                      )}
                    </li>
                  );
                })}
              </ol>
            </div>
          )}

          {/* Explanation */}
          {result.explanation && (
            <div style={{ marginTop: 12, fontSize: 12, color: "#9aa4ad" }}>
              {result.explanation}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
