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
    <div className="max-w-6xl mx-auto px-6 py-12">

      {/* HERO */}
      <div className="text-center mb-10">
        <div className="inline-block bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-semibold mb-4">
          AI-Powered Resume Analysis
        </div>

        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Analyze Your Resume
        </h1>

        <p className="text-gray-500 text-lg max-w-2xl mx-auto">
          Upload your resume and compare it with a job description.
          Get ATS scoring, skill gaps and AI-powered recommendations.
        </p>
      </div>

      {/* ANALYZER CARD */}
      <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-8 max-w-4xl mx-auto">

        <form onSubmit={handleSubmit} className="space-y-6">

          {/* FILE UPLOAD */}
          <div>
            <label className="block font-semibold mb-2">
              Resume
            </label>

            <label className="border-2 border-dashed border-gray-300 rounded-xl p-10 flex flex-col items-center justify-center hover:border-blue-500 transition cursor-pointer bg-gray-50">

              <div className="text-5xl mb-3">📄</div>

              <div className="font-semibold text-gray-700">
                {file ? file.name : "Choose your resume"}
              </div>

              <div className="text-sm text-gray-400 mt-2">
                PDF or DOCX
              </div>

              <input
                type="file"
                accept=".pdf,.docx"
                className="hidden"
                onChange={(e) => setFile(e.target.files[0])}
              />
            </label>
          </div>

          {/* JOB DESCRIPTION */}
          <div>
            <label className="block font-semibold mb-2">
              Job Description
            </label>

            <textarea
              className="w-full border border-gray-300 rounded-xl p-4 focus:ring-2 focus:ring-blue-500 focus:outline-none"
              placeholder="Paste the job description here..."
              rows={8}
              value={jd}
              onChange={(e) => setJd(e.target.value)}
            />
          </div>

          {/* BUTTON */}
          <button
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-xl transition"
          >
            {loading ? "Analyzing Resume..." : "🚀 Analyze Resume"}
          </button>

        </form>
      </div>

      {/* RESULTS */}
      {result && (
        <div className="max-w-5xl mx-auto mt-10">

          <h2 className="text-3xl font-bold mb-6">
            Analysis Results
          </h2>

          {/* SCORE CARDS */}
          <div className="grid md:grid-cols-2 gap-6">

            <ScoreCard
              label="Match Score"
              value={result.match_score}
              icon="🎯"
            />

            <ScoreCard
              label="ATS Score"
              value={result.ats_score}
              icon="🤖"
            />

          </div>

          {/* MISSING SKILLS */}
          <div className="bg-white rounded-2xl shadow border p-6 mt-6">

            <h3 className="text-xl font-bold mb-4">
              Missing Skills
            </h3>

            <div className="flex flex-wrap gap-3">

              {result.missing_skills?.length > 0 ? (
                result.missing_skills.map((skill, index) => (
                  <span
                    key={index}
                    className="bg-red-100 text-red-700 px-4 py-2 rounded-full text-sm font-medium"
                  >
                    {skill}
                  </span>
                ))
              ) : (
                <span className="text-green-600 font-semibold">
                  ✓ No missing skills detected
                </span>
              )}

            </div>
          </div>

          {/* AI FEEDBACK */}
          <div className="bg-white rounded-2xl shadow border p-6 mt-6">

            <h3 className="text-xl font-bold mb-4">
              🧠 AI Feedback
            </h3>

            <div className="space-y-3">

              {result.llm_feedback?.strengths?.length > 0 && (
                <div>
                  <h4 className="font-semibold text-green-600">
                    Strengths
                  </h4>

                  <ul className="list-disc pl-6">
                    {result.llm_feedback.strengths.map((s, i) => (
                      <li key={i}>{s}</li>
                    ))}
                  </ul>
                </div>
              )}

              {result.llm_feedback?.suggestions?.map((s, i) => (
                <div
                  key={i}
                  className="bg-blue-50 p-4 rounded-lg"
                >
                  💡 {s}
                </div>
              ))}

            </div>
          </div>

        </div>
      )}

    </div>
  );
}

function ScoreCard({ label, value, icon }) {
  return (
    <div className="bg-white rounded-2xl shadow border p-8 text-center">

      <div className="text-4xl mb-3">
        {icon}
      </div>

      <div className="text-5xl font-bold text-blue-600">
        {value}%
      </div>

      <div className="text-gray-500 mt-2">
        {label}
      </div>

    </div>
  );
}
