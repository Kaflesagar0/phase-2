import { Link, Outlet } from "react-router-dom";
import { HealthStatus } from "./HealthStatus";

export function AppLayout() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 flex flex-col">
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link to="/" className="flex items-center gap-2 text-xl font-bold text-emerald-700">
              <span role="img" aria-label="sprout">🌱</span> Smart Greenhouse
            </Link>
            <nav className="flex items-center space-x-4 text-sm font-medium">
              <Link to="/" className="text-slate-600 hover:text-emerald-700 transition-colors">
                Home
              </Link>
              <Link to="/dashboard" className="text-slate-600 hover:text-emerald-700 transition-colors">
                Dashboard
              </Link>
            </nav>
          </div>
          <div>
            <HealthStatus />
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  );
}