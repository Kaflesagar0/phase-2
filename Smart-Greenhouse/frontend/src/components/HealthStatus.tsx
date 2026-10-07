import { useEffect, useState } from "react";
import { fetchHealth, type HealthResponse } from "../services/api";

export function HealthStatus() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<boolean>(false);

  useEffect(() => {
    let isMounted = true;

    const checkHealth = () => {
      fetchHealth()
        .then((data) => {
          if (isMounted) {
            setHealth(data);
            setError(false);
          }
        })
        .catch(() => {
          if (isMounted) {
            setError(true);
            setHealth(null);
          }
        });
    };

    checkHealth();
    const interval = setInterval(checkHealth, 5000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  if (error || !health) {
    return (
      <div className="flex items-center gap-2 px-3 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-700 border border-red-300">
        <span className="h-2 w-2 rounded-full bg-red-500 animate-pulse"></span>
        API: Offline
      </div>
    );
  }

  const isHealthy = health.status === "ok" && health.db === "ok";

  return (
    <div
      className={`flex items-center gap-2 px-3 py-1 text-xs font-semibold rounded-full border ${
        isHealthy
          ? "bg-emerald-100 text-emerald-800 border-emerald-300"
          : "bg-amber-100 text-amber-800 border-amber-300"
      }`}
    >
      <span
        className={`h-2 w-2 rounded-full ${
          isHealthy ? "bg-emerald-500" : "bg-amber-500"
        }`}
      ></span>
      <span>
        API: {health.status.toUpperCase()} | DB: {health.db.toUpperCase()}
      </span>
    </div>
  );
}