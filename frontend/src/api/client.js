const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.error || `Request failed (${res.status})`);
  }
  return data;
}

export const api = {
  // Projects
  getProjects: () => request("/api/projects"),
  getProject: (id) => request(`/api/projects/${id}`),
  createProject: (payload) =>
    request("/api/projects", { method: "POST", body: JSON.stringify(payload) }),
  updateProject: (id, payload) =>
    request(`/api/projects/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteProject: (id) => request(`/api/projects/${id}`, { method: "DELETE" }),

  // Tasks
  getTasks: (params = {}) => {
    const qs = new URLSearchParams(params).toString();
    return request(`/api/tasks${qs ? `?${qs}` : ""}`);
  },
  getTask: (id) => request(`/api/tasks/${id}`),
  createTask: (payload) =>
    request("/api/tasks", { method: "POST", body: JSON.stringify(payload) }),
  updateTask: (id, payload) =>
    request(`/api/tasks/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteTask: (id) => request(`/api/tasks/${id}`, { method: "DELETE" }),

  // Comments
  getComments: (taskId) => request(`/api/tasks/${taskId}/comments`),
  addComment: (taskId, payload) =>
    request(`/api/tasks/${taskId}/comments`, { method: "POST", body: JSON.stringify(payload) }),

  // Stats
  getOverview: () => request("/api/stats/overview"),
  getTasksPerWeek: () => request("/api/stats/tasks-per-week"),
  getByPriority: () => request("/api/stats/by-priority"),
};
