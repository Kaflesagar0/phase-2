import { useState, useEffect } from "react";
import { API_BASE_URL } from "../../services/api";

interface ZoneRecommendation {
  zone_id: string;
  zone_name: string;
  action: string;
  reason: string;
  score?: number;
}

interface EvaluationResult {
  location_id: string;
  strategy_key: string;
  recommendations: ZoneRecommendation[];
}

interface StrategyPanelProps {
  locationId: string | null;
}

export function StrategyPanel({ locationId }: StrategyPanelProps) {
  const [strategyKey, setStrategyKey] = useState("conservative");
  const [evaluation, setEvaluation] = useState<EvaluationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    if (locationId) {
      setEvaluation(null);
      setError(null);
      setSuccess(null);
    }
  }, [locationId]);

  const handleSaveStrategy = async () => {
    if (!locationId) return;
    setError(null);
    setSuccess(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/locations/${locationId}/automation/strategy`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ strategy_key: strategyKey }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Failed to save strategy");
      }
      setSuccess("Strategy updated successfully!");
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleEvaluate = async () => {
    if (!locationId) return;
    setError(null);
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/locations/${locationId}/automation/evaluate`, {
        method: "POST",
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Failed to evaluate automation");
      }
      const data: EvaluationResult = await res.json();
      setEvaluation(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!locationId) {
    return (
      <div className="bg-white p-6 rounded-xl border border-slate-200 text-center text-slate-400 text-xs">
        Select a location under Configuration to manage automation strategies.
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 space-y-6">
      <div>
        <h3 className="text-lg font-bold text-slate-900">Automation Strategy Panel</h3>
        <p className="text-xs text-slate-500">Configure evaluation algorithms and trigger real-time zone recommendations.</p>
      </div>

      {error && <div className="p-3 text-xs bg-red-50 text-red-700 border border-red-200 rounded">{error}</div>}
      {success && <div className="p-3 text-xs bg-emerald-50 text-emerald-700 border border-emerald-200 rounded">{success}</div>}

      <div className="flex flex-col sm:flex-row gap-4 items-end">
        <div className="w-full sm:w-auto flex-1">
          <label className="block text-xs font-semibold text-slate-700 mb-1">Active Strategy</label>
          <select
            value={strategyKey}
            onChange={(e) => setStrategyKey(e.target.value)}
            className="w-full px-3 py-2 text-xs rounded border border-slate-200 bg-white"
          >
            <option value="conservative">Conservative (Cautious moisture buffer)</option>
            <option value="aggressive">Aggressive (Strict threshold tracking)</option>
          </select>
        </div>
        <button
          onClick={handleSaveStrategy}
          className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded text-xs font-semibold"
        >
          Save Strategy
        </button>
        <button
          onClick={handleEvaluate}
          disabled={loading}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-xs font-semibold shadow-xs disabled:opacity-50"
        >
          {loading ? "Evaluating..." : "Evaluate Now"}
        </button>
      </div>

      {evaluation && (
        <div className="space-y-4 pt-4 border-t border-slate-100">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Evaluation Results (Strategy: {evaluation.strategy_key})
          </h4>
          <div className="grid grid-cols-1 gap-3">
            {evaluation.recommendations.map((rec) => (
              <div key={rec.zone_id} className="p-4 rounded-lg border border-slate-200 bg-slate-50 flex justify-between items-center">
                <div>
                  <h5 className="font-semibold text-slate-800 text-sm">{rec.zone_name}</h5>
                  <p className="text-xs text-slate-600 mt-1">{rec.reason}</p>
                </div>
                <span
                  className={`px-3 py-1 text-xs font-bold uppercase rounded-full ${
                    rec.action === "irrigate"
                      ? "bg-blue-100 text-blue-800 border border-blue-200"
                      : "bg-amber-100 text-amber-800 border border-amber-200"
                  }`}
                >
                  {rec.action}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}