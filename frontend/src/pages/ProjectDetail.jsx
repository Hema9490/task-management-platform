import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../api/client";
import { StatusBadge, PriorityBadge } from "../components/Badges";

const STATUSES = ["todo", "in_progress", "done"];

export default function ProjectDetail() {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [title, setTitle] = useState("");
  const [priority, setPriority] = useState("medium");
  const [error, setError] = useState("");

  const load = () => api.getProject(id).then(setProject).catch((e) => setError(e.message));

  useEffect(() => { load(); }, [id]);

  const handleCreateTask = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    try {
      await api.createTask({ project_id: Number(id), title, priority });
      setTitle("");
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  const cycleStatus = async (task) => {
    const next = STATUSES[(STATUSES.indexOf(task.status) + 1) % STATUSES.length];
    await api.updateTask(task.id, { status: next });
    load();
  };

  if (!project) {
    return <div className="max-w-6xl mx-auto px-6 py-10 text-mist text-sm">{error || "Loading…"}</div>;
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-10 space-y-8">
      <div>
        <Link to="/projects" className="text-xs font-mono text-mist hover:text-signal">&larr; All projects</Link>
        <h1 className="font-display text-2xl font-semibold mt-2">{project.name}</h1>
        {project.description && <p className="text-mist text-sm mt-1">{project.description}</p>}
      </div>

      <form onSubmit={handleCreateTask} className="bg-panel border border-rail rounded-lg p-5 flex flex-col md:flex-row gap-3">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New task title"
          className="flex-1 bg-ink border border-rail rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-signal"
        />
        <select
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
          className="bg-ink border border-rail rounded-md px-3 py-2 text-sm"
        >
          <option value="low">low</option>
          <option value="medium">medium</option>
          <option value="high">high</option>
        </select>
        <button className="bg-signal text-ink font-medium text-sm px-4 py-2 rounded-md hover:brightness-110 transition">
          Add task
        </button>
      </form>

      <div className="space-y-2">
        {project.tasks?.map((t) => (
          <div key={t.id} className="bg-panel border border-rail rounded-lg px-4 py-3 flex items-center justify-between gap-4">
            <Link to={`/tasks/${t.id}`} className="font-medium text-sm hover:text-signal transition truncate">
              {t.title}
            </Link>
            <div className="flex items-center gap-2 shrink-0">
              <PriorityBadge priority={t.priority} />
              <button onClick={() => cycleStatus(t)} title="Click to advance status">
                <StatusBadge status={t.status} />
              </button>
            </div>
          </div>
        ))}
        {project.tasks?.length === 0 && (
          <p className="text-mist text-sm">No tasks yet — add the first one above.</p>
        )}
      </div>
    </div>
  );
}
