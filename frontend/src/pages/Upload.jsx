import { useState } from "react";
import api from "../api";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [jd, setJd] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please select a resume.");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("job_description", jd);

    try {
      const res = await api.post("/resumes/analyze", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setResult(res.data);
    } catch (err) {
      alert(
        "Analysis failed: " +
        (err.response?.data?.detail || err.message)
      );
    }

    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">
        Analyze Your Resume
      </h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="file"
          accept=".pdf,.docx"
          onChange={(e) => setFile(e.target.files[0])}
          required
        />

        <textarea
          className="w-full border rounded p-2"
          placeholder="Paste job description (optional, for match scoring)"
          rows={6}
          value={jd}
          onChange={(e) => setJd(e.target.value)}
        />

        <button
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {result && (
        <div className="mt-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <ScoreCard
              label="Match Score"
              value={result.match_score}
            />

            <ScoreCard
              label="ATS Score"
              value={result.ats_score}
            />
          </div>

          <div>
            <h3 className="font-semibold">
              Missing Skills
            </h3>

            <p>
              {result.missing_skills?.join(", ") ||
                "None detected"}
            </p>
          </div>

          <div>
            <h3 className="font-semibold">
              AI Feedback
            </h3>

            <p className="text-sm text-gray-700">
              {result.llm_feedback?.overall_summary ||
                "AI feedback generated."}
            </p>

            <ul className="list-disc pl-5 mt-2">
              {result.llm_feedback?.suggestions?.map(
                (s, i) => (
                  <li key={i}>{s}</li>
                )
              )}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

function ScoreCard({ label, value }) {
  return (
    <div className="border rounded p-4 text-center">
      <div className="text-3xl font-bold">
        {value}%
      </div>

      <div className="text-sm text-gray-500">
        {label}
      </div>
    </div>
  );
}
