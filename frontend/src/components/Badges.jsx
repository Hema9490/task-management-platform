const STATUS_STYLES = {
  todo: "bg-mist/15 text-mist",
  in_progress: "bg-signal/15 text-signal",
  done: "bg-go/15 text-go",
};

const STATUS_LABEL = {
  todo: "To do",
  in_progress: "In progress",
  done: "Done",
};

const PRIORITY_STYLES = {
  low: "border-mist/40 text-mist",
  medium: "border-signal/40 text-signal",
  high: "border-stop/40 text-stop",
};

export function StatusBadge({ status }) {
  return (
    <span className={`text-xs font-mono px-2 py-0.5 rounded ${STATUS_STYLES[status] || STATUS_STYLES.todo}`}>
      {STATUS_LABEL[status] || status}
    </span>
  );
}

export function PriorityBadge({ priority }) {
  return (
    <span className={`text-xs font-mono px-2 py-0.5 rounded border ${PRIORITY_STYLES[priority] || PRIORITY_STYLES.medium}`}>
      {priority}
    </span>
  );
}
