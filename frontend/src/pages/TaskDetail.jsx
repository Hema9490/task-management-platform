import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../api/client";
import { StatusBadge, PriorityBadge } from "../components/Badges";

export default function TaskDetail() {
  const { id } = useParams();
  const [task, setTask] = useState(null);
  const [body, setBody] = useState("");
  const [author, setAuthor] = useState("");
  const [error, setError] = useState("");

  const load = () => api.getTask(id).then(setTask).catch((e) => setError(e.message));

  useEffect(() => { load(); }, [id]);

  const handleComment = async (e) => {
    e.preventDefault();
    if (!body.trim()) return;
    try {
      await api.addComment(id, { body, author: author || "Anonymous" });
      setBody("");
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  if (!task) {
    return <div className="max-w-3xl mx-auto px-6 py-10 text-mist text-sm">{error || "Loading…"}</div>;
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-10 space-y-6">
      <Link to={`/projects/${task.project_id}`} className="text-xs font-mono text-mist hover:text-signal">
        &larr; Back to project
      </Link>

      <div className="bg-panel border border-rail rounded-lg p-5">
        <div className="flex items-center gap-2 mb-2">
          <StatusBadge status={task.status} />
          <PriorityBadge priority={task.priority} />
        </div>
        <h1 className="font-display text-xl font-semibold">{task.title}</h1>
        {task.description && <p className="text-mist text-sm mt-2">{task.description}</p>}
        {task.assignee && <p className="text-xs font-mono text-mist mt-3">Assigned to {task.assignee}</p>}
      </div>

      <div>
        <h2 className="text-sm font-mono text-mist mb-3">Comments</h2>
        <div className="space-y-2">
          {task.comments?.map((c) => (
            <div key={c.id} className="bg-panel border border-rail rounded-lg px-4 py-3">
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium">{c.author}</span>
                <span className="text-xs font-mono text-mist">{new Date(c.created_at).toLocaleString()}</span>
              </div>
              <p className="text-sm text-slate-200">{c.body}</p>
            </div>
          ))}
          {task.comments?.length === 0 && <p className="text-mist text-sm">No comments yet.</p>}
        </div>

        <form onSubmit={handleComment} className="mt-4 space-y-2">
          <input
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
            placeholder="Your name"
            className="w-full bg-ink border border-rail rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-signal"
          />
          <textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            placeholder="Add a comment…"
            rows={3}
            className="w-full bg-ink border border-rail rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-signal"
          />
          <button className="bg-signal text-ink font-medium text-sm px-4 py-2 rounded-md hover:brightness-110 transition">
            Post comment
          </button>
        </form>
      </div>
    </div>
  );
}
