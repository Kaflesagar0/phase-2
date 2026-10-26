import { useEffect, useState } from "react";
import { fetchLocations, fetchLocationOverview, type LocationMetadataDto, type LocationOverviewDto } from "../../services/api";

export function OverviewPanel() {
  const [locations, setLocations] = useState<LocationMetadataDto[]>([]);
  const [selectedLocationId, setSelectedLocationId] = useState<string>("");
  const [overview, setOverview] = useState<LocationOverviewDto | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchLocations()
      .then((locs) => {
        setLocations(locs);
        if (locs.length > 0) {
          setSelectedLocationId(locs[0].id);
        }
      })
      .catch((err) => setError(err.message));
  }, []);

  const loadOverview = async (locId: string) => {
    if (!locId) return;
    try {
      setLoading(true);
      setError(null);
      const data = await fetchLocationOverview(locId);
      setOverview(data);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to load overview");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedLocationId) {
      loadOverview(selectedLocationId);
    }
  }, [selectedLocationId]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Dashboard Overview</h2>
          <p className="text-sm text-slate-500">Aggregated real-time greenhouse metrics</p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={selectedLocationId}
            onChange={(e) => setSelectedLocationId(e.target.value)}
            className="px-3 py-1.5 text-sm rounded-lg border border-slate-300 bg-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
          >
            {locations.map((loc) => (
              <option key={loc.id} value={loc.id}>
                {loc.name}
              </option>
            ))}
          </select>
          <button
            onClick={() => loadOverview(selectedLocationId)}
            disabled={loading || !selectedLocationId}
            className="px-3 py-1.5 text-sm font-medium rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 disabled:opacity-50 transition-colors"
          >
            Refresh
          </button>
        </div>
      </div>

      {error && (
        <div className="p-3 text-sm rounded-lg bg-red-50 text-red-700 border border-red-200">
          {error}
        </div>
      )}

      {loading && !overview && (
        <p className="text-sm text-slate-500 py-8">Loading overview snapshot...</p>
      )}

      {overview && (
        <div className="space-y-6">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-xs">
              <span className="text-xs font-medium text-slate-500 uppercase tracking-wider">Assigned Sensors</span>
              <p className="text-2xl font-bold text-slate-900 mt-1">{overview.device_counts.sensor}</p>
            </div>
            <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-xs">
              <span className="text-xs font-medium text-slate-500 uppercase tracking-wider">Assigned Actuators</span>
              <p className="text-2xl font-bold text-slate-900 mt-1">{overview.device_counts.actuator}</p>
            </div>
            <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-xs">
              <span className="text-xs font-medium text-slate-500 uppercase tracking-wider">Active Strategy</span>
              <p className="text-lg font-semibold text-emerald-700 mt-1 capitalize">
                {overview.strategy_key || "None saved"}
              </p>
              {overview.last_recommendation && (
                <p className="text-xs text-slate-600 mt-1">
                  <strong className="uppercase">{overview.last_recommendation.action}:</strong> {overview.last_recommendation.reason}
                </p>
              )}
            </div>
          </div>

          {/* Zones List */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-slate-800">Zones ({overview.zones.length})</h3>
            {overview.zones.length === 0 ? (
              <p className="text-sm text-slate-400">No zones configured for this location.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {overview.zones.map((zone) => (
                  <div key={zone.id} className="p-5 rounded-xl bg-white border border-slate-200 shadow-xs space-y-4">
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-bold text-slate-900">{zone.name}</h4>
                        <span className="text-xs text-slate-500">
                          Thresholds: {zone.moisture_threshold_low} - {zone.moisture_threshold_high} VWC
                        </span>
                      </div>
                    </div>

                    {/* Devices in Zone */}
                    <div className="space-y-2">
                      <h5 className="text-xs font-semibold text-slate-600 uppercase">Assigned Devices ({zone.devices.length})</h5>
                      {zone.devices.length === 0 ? (
                        <p className="text-xs text-slate-400">No devices assigned.</p>
                      ) : (
                        <div className="space-y-1.5">
                          {zone.devices.map((dev) => {
                            const reading = zone.latest_readings.find((r) => r.device_id === dev.id);
                            return (
                              <div key={dev.id} className="p-2 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-between text-xs">
                                <div>
                                  <span className="font-semibold text-slate-800">{dev.display_name}</span>
                                  <span className="ml-2 text-slate-400 capitalize">({dev.role})</span>
                                </div>
                                <div>
                                  {reading ? (
                                    <span className="font-mono font-medium text-emerald-700">
                                      {reading.value} {reading.unit}
                                    </span>
                                  ) : (
                                    <span className="text-slate-400 italic">No reading</span>
                                  )}
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}