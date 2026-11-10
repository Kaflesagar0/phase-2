import { useEffect, useState } from "react";

export interface ExecutionLogItem {
  id: string;
  device_id: string;
  success: boolean;
  policy_applied: string[];
  message: string | null;
  created_at: string;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export function ExecutionLog() {
  const [logs, setLogs] = useState<ExecutionLogItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const res = await fetch(`${API_BASE_URL}/api/actuators/executions?limit=20`);
      if (!res.ok) throw new Error("Failed to fetch execution logs");
      const data = await res.json();
      setLogs(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Error loading logs");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-800">Actuator Execution Log</h2>
          <p className="text-xs text-slate-500">
            Any command succeeds until the actuator has been running for 30 minutes. Successful rows show empty messages and logging policy; blocked rows show policy metadata and error messages.
          </p>
        </div>
        <button
          onClick={fetchLogs}
          className="px-3 py-1.5 text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors"
        >
          Refresh Log
        </button>
      </div>

      {error && <div className="p-3 text-xs text-red-600 bg-red-50 border border-red-200 rounded-lg">{error}</div>}

      {loading && logs.length === 0 ? (
        <div className="text-sm text-slate-400 py-6 text-center">Loading execution history...</div>
      ) : logs.length === 0 ? (
        <div className="text-center py-8 bg-slate-50 rounded-xl border border-dashed border-slate-200">
          <p className="text-sm font-medium text-slate-600">No execution logs recorded yet.</p>
          <p className="text-xs text-slate-400 mt-1">Commands dispatched through decorated ports will appear here.</p>
        </div>
      ) : (
        <div className="overflow-x-auto border border-slate-200 rounded-xl">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-50 text-slate-600 border-b border-slate-200 font-semibold">
                <th className="p-3">Status</th>
                <th className="p-3">Device ID</th>
                <th className="p-3">Policies Applied</th>
                <th className="p-3">Message</th>
                <th className="p-3">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-50/50 transition-colors">
                  <td className="p-3">
                    <span
                      className={`px-2 py-0.5 rounded-full font-mono font-bold uppercase text-[10px] ${
                        log.success
                          ? "bg-emerald-100 text-emerald-800 border border-emerald-200"
                          : "bg-red-100 text-red-800 border border-red-200"
                      }`}
                    >
                      {log.success ? "Success" : "Blocked"}
                    </span>
                  </td>
                  <td className="p-3 font-mono text-slate-600">{log.device_id}</td>
                  <td className="p-3">
                    <div className="flex flex-wrap gap-1">
                      {log.policy_applied.map((policy, idx) => (
                        <span key={idx} className="px-1.5 py-0.5 bg-slate-100 text-slate-600 rounded font-mono">
                          {policy}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="p-3 text-slate-600 italic">{log.message || "—"}</td>
                  <td className="p-3 text-slate-400 font-mono">
                    {new Date(log.created_at).toLocaleTimeString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}