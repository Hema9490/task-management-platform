import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");

  const load = () => api.getProjects().then(setProjects).catch((e) => setError(e.message));

  useEffect(() => { load(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    try {
      await api.createProject({ name, description });
      setName("");
      setDescription("");
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-6 py-10 space-y-8">
      <div>
        <h1 className="font-display text-2xl font-semibold">Projects</h1>
        <p className="text-mist text-sm mt-1">Everything you're actively shipping.</p>
      </div>

      <form onSubmit={handleCreate} className="bg-panel border border-rail rounded-lg p-5 flex flex-col md:flex-row gap-3">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Project name"
          className="flex-1 bg-ink border border-rail rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-signal"
        />
        <input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Short description (optional)"
          className="flex-1 bg-ink border border-rail rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-signal"
        />
        <button className="bg-signal text-ink font-medium text-sm px-4 py-2 rounded-md hover:brightness-110 transition">
          New project
        </button>
      </form>

      {error && <p className="text-stop text-sm font-mono">{error}</p>}

      <div className="grid md:grid-cols-2 gap-4">
        {projects.map((p) => (
          <Link
            key={p.id}
            to={`/projects/${p.id}`}
            className="bg-panel border border-rail rounded-lg p-5 hover:border-signal/50 transition block"
          >
            <div className="flex items-start justify-between">
              <h2 className="font-display font-semibold">{p.name}</h2>
              <span className="text-xs font-mono text-mist">{p.status}</span>
            </div>
            {p.description && <p className="text-sm text-mist mt-2">{p.description}</p>}
            <p className="text-xs font-mono text-signal mt-4">{p.task_count} task{p.task_count === 1 ? "" : "s"}</p>
          </Link>
        ))}
        {projects.length === 0 && (
          <p className="text-mist text-sm">No projects yet — create your first one above.</p>
        )}
      </div>
    </div>
  );
}
