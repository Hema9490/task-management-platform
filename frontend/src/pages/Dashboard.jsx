import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip,
  PieChart, Pie, Cell,
} from "recharts";
import { api } from "../api/client";
import StatCard from "../components/StatCard";

const PRIORITY_COLORS = { high: "#E0556F", medium: "#E8A33D", low: "#8A96A3" };

export default function Dashboard() {
  const [overview, setOverview] = useState(null);
  const [weekly, setWeekly] = useState([]);
  const [byPriority, setByPriority] = useState({});
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([api.getOverview(), api.getTasksPerWeek(), api.getByPriority()])
      .then(([ov, wk, pr]) => {
        setOverview(ov);
        setWeekly(wk);
        setByPriority(pr);
      })
      .catch((e) => setError(e.message));
  }, []);

  const priorityData = Object.entries(byPriority).map(([name, value]) => ({ name, value }));

  if (error) {
    return (
      <div className="max-w-6xl mx-auto px-6 py-10">
        <p className="text-stop font-mono text-sm">
          Couldn't reach the API: {error}. Is the backend running?
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-10 space-y-8">
      <div>
        <h1 className="font-display text-2xl font-semibold">Dashboard</h1>
        <p className="text-mist text-sm mt-1">Live snapshot across every project.</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard label="Projects" value={overview?.total_projects ?? "—"} />
        <StatCard label="Total tasks" value={overview?.total_tasks ?? "—"} />
        <StatCard label="Completion rate" value={overview ? `${overview.completion_rate_pct}%` : "—"} accent="text-go" />
        <StatCard
          label="Avg close time"
          value={overview?.avg_close_time_hours != null ? `${overview.avg_close_time_hours}h` : "—"}
          accent="text-signal"
        />
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-panel border border-rail rounded-lg p-5">
          <p className="text-sm font-mono text-mist mb-4">Tasks created / week</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={weekly}>
              <XAxis dataKey="week" stroke="#8A96A3" fontSize={11} />
              <YAxis stroke="#8A96A3" fontSize={11} allowDecimals={false} />
              <Tooltip contentStyle={{ background: "#161F2B", border: "1px solid #1F2A38" }} />
              <Bar dataKey="count" fill="#E8A33D" radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-panel border border-rail rounded-lg p-5">
          <p className="text-sm font-mono text-mist mb-4">Tasks by priority</p>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={priorityData} dataKey="value" nameKey="name" innerRadius={50} outerRadius={80} paddingAngle={3}>
                {priorityData.map((entry) => (
                  <Cell key={entry.name} fill={PRIORITY_COLORS[entry.name] || "#8A96A3"} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: "#161F2B", border: "1px solid #1F2A38" }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
