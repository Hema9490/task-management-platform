import { NavLink } from "react-router-dom";

const linkClass = ({ isActive }) =>
  `px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
    isActive ? "bg-signal/15 text-signal" : "text-mist hover:text-slate-100"
  }`;

export default function Navbar() {
  return (
    <header className="border-b border-rail bg-panel/60 backdrop-blur sticky top-0 z-10">
      <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-signal" />
          <span className="font-display font-semibold tracking-tight">Control Board</span>
        </div>
        <nav className="flex items-center gap-1">
          <NavLink to="/" end className={linkClass}>Dashboard</NavLink>
          <NavLink to="/projects" className={linkClass}>Projects</NavLink>
        </nav>
      </div>
    </header>
  );
}
