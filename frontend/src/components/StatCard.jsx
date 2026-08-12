export default function StatCard({ label, value, accent = "text-slate-100" }) {
  return (
    <div className="bg-panel border border-rail rounded-lg px-5 py-4">
      <p className="text-xs uppercase tracking-wider text-mist font-mono mb-1">{label}</p>
      <p className={`text-3xl font-display font-semibold ${accent}`}>{value}</p>
    </div>
  );
}
