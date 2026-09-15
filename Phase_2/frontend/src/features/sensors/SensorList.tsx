import { useEffect, useState } from "react";
import { fetchSensors, createSensor, type SensorDto } from "../../services/api";

export function SensorList() {
  const [sensors, setSensors] = useState<SensorDto[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);

  const loadSensors = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchSensors();
      setSensors(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load sensors");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSensors();
  }, []);

  const handleAddSensor = async (type: "moisture" | "light") => {
    try {
      setCreating(true);
      setError(null);
      await createSensor({ type });
      await loadSensors();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Creation failed");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-800">Sensors</h2>
          <p className="text-xs text-slate-500">Heterogeneous greenhouse sensors</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => handleAddSensor("moisture")}
            disabled={creating}
            className="px-2.5 py-1 text-xs font-medium rounded bg-emerald-600 text-white hover:bg-emerald-700 disabled:opacity-50"
          >
            + Moisture
          </button>
          <button
            onClick={() => handleAddSensor("light")}
            disabled={creating}
            className="px-2.5 py-1 text-xs font-medium rounded bg-amber-600 text-white hover:bg-amber-700 disabled:opacity-50"
          >
            + Light
          </button>
        </div>
      </div>

      {error && (
        <div className="p-2 text-xs rounded bg-red-50 text-red-700 border border-red-200">
          {error}
        </div>
      )}

      {loading ? (
        <p className="text-xs text-slate-400 py-4">Loading sensors...</p>
      ) : sensors.length === 0 ? (
        <div className="text-center py-6 border border-dashed border-slate-200 rounded-lg">
          <p className="text-xs text-slate-400">No sensors registered.</p>
        </div>
      ) : (
        <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
          {sensors.map((s) => (
            <div key={s.id} className="p-2.5 rounded border border-slate-100 bg-slate-50 text-xs flex flex-col gap-1">
              <div className="flex justify-between items-center">
                <span className="font-semibold text-slate-700">{s.display_name}</span>
                <span className="font-mono text-[10px] text-slate-400">{s.device_type}</span>
              </div>
              <pre className="text-[10px] text-slate-500 bg-white p-1.5 rounded border border-slate-200 overflow-x-auto">
                {JSON.stringify(s.default_config, null, 2)}
              </pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}