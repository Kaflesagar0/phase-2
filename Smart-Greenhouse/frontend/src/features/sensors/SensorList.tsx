import { useEffect, useState } from "react";
import { fetchSensors, createSensor, triggerSensorRead, fetchSensorReadings,  updateDeviceSampling, type ReadingDto, type SensorDto } from "../../services/api";

export function SensorList() {
  const [sensors, setSensors] = useState<SensorDto[]>([]);
  const [readings, setReadings] = useState<Record<string, ReadingDto>>({});
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [displayName, setDisplayName] = useState<string>("");
  

  const loadSensorsAndReadings = async () => {
    try {
      setLoading(true);
      const sensorData = await fetchSensors();
      setSensors(sensorData);

      // Fetch latest reading for each sensor
      const readingsMap: Record<string, ReadingDto> = {};
      for (const sensor of sensorData) {
        try {
          const res = await fetchSensorReadings(sensor.id, 1);
          if (res.length > 0) {
            readingsMap[sensor.id] = res[0];
          }
        } catch {
          // Ignore individual fetch errors if no readings exist yet
        }
      }
      setReadings(readingsMap);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to load sensors");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSensorsAndReadings();

    
    const pollInterval = setInterval(async () => {
      try {
        const sensorData = await fetchSensors();
        const readingsMap: Record<string, ReadingDto> = {};
        for (const sensor of sensorData) {
          const res = await fetchSensorReadings(sensor.id, 1);
          if (res.length > 0) {
            readingsMap[sensor.id] = res[0];
          }
        }
        setReadings(readingsMap);
      } catch {
        
      }
    }, 5000);

    return () => clearInterval(pollInterval);
  }, []);

  const handleReadNow = async (deviceId: string) => {
    try {
      const newReading = await triggerSensorRead(deviceId);
      setReadings((prev) => ({ ...prev, [deviceId]: newReading }));
    } catch (err: any) {
      setError(err.message || "Failed to execute manual read");
    }
  };

  const handleSamplingChange = async (
    deviceId: string,
    interval: number,
    tracking: boolean
  ) => {
    try {
      await updateDeviceSampling(deviceId, interval, tracking);
      await loadSensorsAndReadings();
    } catch (err: any) {
      setError(err.message || "Failed to update sampling settings");
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-800">Sensors</h2>
          <p className="text-sm text-slate-500">Manage sensors, readings, and intervals.</p>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row gap-2 items-stretch sm:items-center">
        <input
          type="text"
          placeholder="Display name (optional)"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          className="px-3 py-1.5 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
        />
        <div className="flex gap-2">
          <button
            onClick={async () => {
              await createSensor({ type: "moisture", display_name: displayName || undefined });
              setDisplayName("");
              loadSensorsAndReadings();
            }}
            className="px-3 py-1.5 bg-emerald-600 text-white text-sm font-medium rounded-lg hover:bg-emerald-700 transition-colors"
          >
            Add Moisture
          </button>
          <button
            onClick={async () => {
              await createSensor({ type: "light", display_name: displayName || undefined });
              setDisplayName("");
              loadSensorsAndReadings();
            }}
            className="px-3 py-1.5 bg-amber-600 text-white text-sm font-medium rounded-lg hover:bg-amber-700 transition-colors"
          >
            Add Light
          </button>
        </div>
      </div>

      {error && (
        <div className="p-3 text-sm text-red-700 bg-red-50 border border-red-200 rounded-lg">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-sm text-slate-400 py-4 text-center">Loading sensors...</div>
      ) : sensors.length === 0 ? (
        <div className="text-sm text-slate-400 py-8 text-center border border-dashed border-slate-200 rounded-lg">
          No sensors registered yet. Add one above!
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {sensors.map((sensor) => {
            const latest = readings[sensor.id];
            const interval = (sensor.default_config?.sampling_interval_seconds as number) ?? 300;
            const tracking = (sensor.default_config?.tracking_enabled as boolean) ?? true;

            return (
              <div
                key={sensor.id}
                className="p-4 border border-slate-200 rounded-lg bg-slate-50/50 flex flex-col gap-3"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-slate-800">
                    {sensor.display_name || sensor.device_type}
                  </span>
                  <div className="flex items-center gap-2">
                    {latest && (
                      <span className="px-2 py-0.5 text-xs font-semibold bg-emerald-100 text-emerald-800 rounded">
                        {latest.value} {latest.unit}
                      </span>
                    )}
                    {latest && (
                      <span className="px-2 py-0.5 text-xs font-mono uppercase bg-slate-200 text-slate-700 rounded">
                        {latest.source}
                      </span>
                    )}
                  </div>
                </div>

                <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-200/60 text-xs text-slate-600">
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => handleReadNow(sensor.id)}
                      className="px-2.5 py-1 bg-slate-800 text-white rounded font-medium hover:bg-slate-900 transition-colors"
                    >
                      Read Now
                    </button>
                    <label className="flex items-center gap-1.5">
                      <span>Interval (s):</span>
                      <input
                        type="number"
                        min="5"
                        defaultValue={interval}
                        onBlur={(e) =>
                          handleSamplingChange(
                            sensor.id,
                            Math.max(5, parseInt(e.target.value) || 300),
                            tracking
                          )
                        }
                        className="w-16 px-1.5 py-0.5 border border-slate-300 rounded bg-white text-center font-mono"
                      />
                    </label>
                  </div>
                  <label className="flex items-center gap-1.5 cursor-pointer">
                    <input
                      type="checkbox"
                      defaultChecked={tracking}
                      onChange={(e) =>
                        handleSamplingChange(sensor.id, interval, e.target.checked)
                      }
                      className="rounded border-slate-300 text-emerald-600 focus:ring-emerald-500"
                    />
                    <span>Tracking Enabled</span>
                  </label>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}