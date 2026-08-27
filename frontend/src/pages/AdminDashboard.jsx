import { useEffect, useState } from "react";
import api from "../api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function AdminDashboard() {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadData = async () => {
      try {
        const res = await api.get("/admin/analyses");
        setCandidates(res.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
          "Failed to load admin data"
        );
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return <p className="p-6">Loading...</p>;
  }

  if (error) {
    return <p className="p-6 text-red-600">{error}</p>;
  }

  const avgMatch =
    candidates.length > 0
      ? (
          candidates.reduce(
            (sum, c) => sum + (c.match_score || 0),
            0
          ) / candidates.length
        ).toFixed(2)
      : "0.00";

  const avgAts =
    candidates.length > 0
      ? (
          candidates.reduce(
            (sum, c) => sum + (c.ats_score || 0),
            0
          ) / candidates.length
        ).toFixed(2)
      : "0.00";

  const skillCounts = {};

  candidates.forEach((candidate) => {
    (candidate.missing_skills || []).forEach((skill) => {
      skillCounts[skill] =
        (skillCounts[skill] || 0) + 1;
    });
  });

  const chartData = Object.entries(skillCounts).map(
    ([skill, count]) => ({
      skill,
      count,
    })
  );

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">
        Recruiter Dashboard
      </h1>

      <div className="grid grid-cols-3 gap-4 mb-8">
        <StatCard
          label="Total Analyses"
          value={candidates.length}
        />

        <StatCard
          label="Avg Match Score"
          value={`${avgMatch}%`}
        />

        <StatCard
          label="Avg ATS Score"
          value={`${avgAts}%`}
        />
      </div>

      <h2 className="font-semibold mb-2">
        Top Missing Skills
      </h2>

      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={chartData}>
          <XAxis dataKey="skill" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" />
        </BarChart>
      </ResponsiveContainer>

      <h2 className="font-semibold mt-8 mb-2">
        Analyses
      </h2>

      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="border-b">
            <th className="py-2">Analysis ID</th>
            <th>Resume ID</th>
            <th>Match %</th>
            <th>ATS %</th>
          </tr>
        </thead>

        <tbody>
          {candidates.map((c) => (
            <tr
              key={c.id}
              className="border-b"
            >
              <td className="py-2">{c.id}</td>
              <td>{c.resume_id}</td>
              <td>{c.match_score}</td>
              <td>{c.ats_score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function StatCard({ label, value }) {
  return (
    <div className="border rounded p-4 text-center">
      <div className="text-2xl font-bold">
        {value}
      </div>

      <div className="text-sm text-gray-500">
        {label}
      </div>
    </div>
  );
}
