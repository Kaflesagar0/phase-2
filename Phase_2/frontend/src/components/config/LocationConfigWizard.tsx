import { useEffect, useState } from "react";
import {
  fetchLocations,
  fetchLocationConfig,
  createLocationConfig,
  deleteLocation,
  addZone,
  editZone,
  deleteZone,
  assignDeviceZone,
  fetchDevices,
  type LocationMetadataDto,
  type LocationConfigDto,
  type ZoneDto,
  type DeviceDto,
} from "../../services/api";

export function LocationConfigWizard() {
  const [locations, setLocations] = useState<LocationMetadataDto[]>([]);
  const [selectedLocationId, setSelectedLocationId] = useState<string | null>(null);
  const [currentConfig, setCurrentConfig] = useState<LocationConfigDto | null>(null);
  const [devices, setDevices] = useState<DeviceDto[]>([]);
  
  // New Location Form State
  const [newLocName, setNewLocName] = useState("");
  const [newZones] = useState<Array<{ name: string; low: number; high: number }>>([
    { name: "Zone 1", low: 0.3, high: 0.7 },
  ]);

  // Zone Add/Edit Form State
  const [zoneModalMode, setZoneModalMode] = useState<"add" | "edit" | null>(null);
  const [editingZone, setEditingZone] = useState<ZoneDto | null>(null);
  const [zoneNameInput, setZoneNameInput] = useState("");
  const [zoneLowInput, setZoneLowInput] = useState("0.3");
  const [zoneHighInput, setZoneHighInput] = useState("0.7");

  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const loadData = async () => {
    try {
      const locs = await fetchLocations();
      setLocations(locs);
      const devs = await fetchDevices();
      setDevices(devs);
      if (locs.length > 0 && !selectedLocationId) {
        setSelectedLocationId(locs[0].id);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    if (selectedLocationId) {
      fetchLocationConfig(selectedLocationId)
        .then(setCurrentConfig)
        .catch((err) => setError(err.message));
    } else {
      setCurrentConfig(null);
    }
  }, [selectedLocationId]);

  const handleCreateLocation = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg(null);
    try {
      const payload = {
        location_name: newLocName,
        zones: newZones.map((z) => ({
          name: z.name,
          moisture_threshold_low: Number(z.low),
          moisture_threshold_high: Number(z.high),
          schedule: {},
        })),
      };
      const created = await createLocationConfig(payload);
      setLocations(await fetchLocations());
      setSelectedLocationId(created.location.id);
      setNewLocName("");
      setSuccessMsg("Location configuration created successfully!");
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleDeleteLocation = async (id: string) => {
    if (!window.confirm("Are you sure you want to delete this location?")) return;
    try {
      await deleteLocation(id);
      const remaining = await fetchLocations();
      setLocations(remaining);
      if (selectedLocationId === id) {
        setSelectedLocationId(remaining.length > 0 ? remaining[0].id : null);
      }
      setSuccessMsg("Location deleted.");
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleSaveZone = async () => {
    if (!selectedLocationId) return;
    setError(null);
    try {
      const payload = {
        name: zoneNameInput,
        moisture_threshold_low: Number(zoneLowInput),
        moisture_threshold_high: Number(zoneHighInput),
        schedule: {},
      };
      if (zoneModalMode === "add") {
        await addZone(selectedLocationId, payload);
      } else if (zoneModalMode === "edit" && editingZone) {
        await editZone(selectedLocationId, editingZone.id, payload);
      }
      const updated = await fetchLocationConfig(selectedLocationId);
      setCurrentConfig(updated);
      setZoneModalMode(null);
      setSuccessMsg("Zone saved successfully.");
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleDeleteZone = async (zoneId: string) => {
    if (!selectedLocationId) return;
    try {
      await deleteZone(selectedLocationId, zoneId);
      const updated = await fetchLocationConfig(selectedLocationId);
      setCurrentConfig(updated);
      setDevices(await fetchDevices()); // Refresh device unassignments
      setSuccessMsg("Zone deleted and associated devices unassigned.");
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleAssignDevice = async (deviceId: string, zoneId: string | null) => {
    try {
      await assignDeviceZone(deviceId, zoneId);
      setDevices(await fetchDevices());
      setSuccessMsg("Device assignment updated.");
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Location & Zone Configuration</h2>
          <p className="text-sm text-slate-500">Manage greenhouse locations, zones, and device assignments.</p>
        </div>
      </div>

      {error && <div className="p-3 text-xs bg-red-50 text-red-700 border border-red-200 rounded">{error}</div>}
      {successMsg && <div className="p-3 text-xs bg-emerald-50 text-emerald-700 border border-emerald-200 rounded">{successMsg}</div>}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Locations List & Selector */}
        <div className="bg-white p-4 rounded-xl border border-slate-200 space-y-4">
          <h3 className="font-semibold text-slate-800">Saved Locations</h3>
          <div className="space-y-2 max-h-60 overflow-y-auto">
            {locations.length === 0 ? (
              <p className="text-xs text-slate-400">No locations configured yet.</p>
            ) : (
              locations.map((loc) => (
                <div
                  key={loc.id}
                  onClick={() => setSelectedLocationId(loc.id)}
                  className={`p-3 rounded-lg border cursor-pointer flex justify-between items-center transition-all ${
                    selectedLocationId === loc.id
                      ? "border-emerald-500 bg-emerald-50/50 text-emerald-900 font-medium"
                      : "border-slate-100 hover:bg-slate-50 text-slate-700"
                  }`}
                >
                  <span className="truncate">{loc.name}</span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteLocation(loc.id);
                    }}
                    className="text-xs text-red-500 hover:text-red-700 px-2 py-1"
                  >
                    Delete
                  </button>
                </div>
              ))
            )}
          </div>

          <hr className="border-slate-100" />

          {/* Quick Create Location Form */}
          <form onSubmit={handleCreateLocation} className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">Add New Location</h4>
            <input
              type="text"
              placeholder="Location Name"
              value={newLocName}
              onChange={(e) => setNewLocName(e.target.value)}
              required
              className="w-full px-3 py-1.5 text-xs rounded border border-slate-200"
            />
            <button
              type="submit"
              className="w-full py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-xs font-semibold shadow-xs"
            >
              Create Location Config
            </button>
          </form>
        </div>

        {/* Selected Location Zones & Details */}
        <div className="lg:col-span-2 bg-white p-4 rounded-xl border border-slate-200 space-y-4">
          {currentConfig ? (
            <div>
              <div className="flex justify-between items-center mb-4">
                <div>
                  <h3 className="text-lg font-bold text-slate-800">{currentConfig.location.name}</h3>
                  <span className="text-xs font-mono text-slate-400">ID: {currentConfig.location.id}</span>
                </div>
                <button
                  onClick={() => {
                    setZoneModalMode("add");
                    setZoneNameInput("");
                    setZoneLowInput("0.3");
                    setZoneHighInput("0.7");
                  }}
                  className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-xs font-semibold"
                >
                  + Add Zone
                </button>
              </div>

              <div className="space-y-3">
                {currentConfig.zones.map((zone) => (
                  <div key={zone.id} className="p-4 rounded-lg border border-slate-200 bg-slate-50 flex flex-col gap-2">
                    <div className="flex justify-between items-center">
                      <span className="font-semibold text-slate-800">{zone.name}</span>
                      <div className="flex gap-2">
                        <button
                          onClick={() => {
                            setZoneModalMode("edit");
                            setEditingZone(zone);
                            setZoneNameInput(zone.name);
                            setZoneLowInput(zone.moisture_threshold_low.toString());
                            setZoneHighInput(zone.moisture_threshold_high.toString());
                          }}
                          className="text-xs text-blue-600 hover:underline"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDeleteZone(zone.id)}
                          className="text-xs text-red-600 hover:underline"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                    <div className="text-xs text-slate-600 flex gap-4">
                      <span>Low Threshold: {zone.moisture_threshold_low}</span>
                      <span>High Threshold: {zone.moisture_threshold_high}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <p className="text-xs text-slate-400 py-12 text-center">Select a location to view its configuration.</p>
          )}
        </div>
      </div>

      {/* Device Zone Assignment Section */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 space-y-4">
        <h3 className="font-semibold text-slate-800">Device Zone Assignments</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {devices.map((dev) => (
            <div key={dev.id} className="p-3 rounded border border-slate-200 bg-slate-50 flex flex-col gap-2">
              <div className="flex justify-between items-center">
                <span className="font-semibold text-slate-700">{dev.display_name || dev.device_type}</span>
                <span className="text-[10px] uppercase px-1.5 py-0.5 rounded bg-slate-200 text-slate-700 font-mono">
                  {dev.role}
                </span>
              </div>
              <div className="text-xs text-slate-500">
                Current Zone ID: <span className="font-mono">{dev.zone_id || "Unassigned"}</span>
              </div>
              <select
                value={dev.zone_id || ""}
                onChange={(e) => handleAssignDevice(dev.id, e.target.value ? e.target.value : null)}
                className="w-full px-2 py-1 text-xs rounded border border-slate-200 bg-white"
              >
                <option value="">-- Unassigned --</option>
                {locations.map((loc) => (
                  // Here we can fetch or group zones across all loaded locations if desired,
                  // or map current location's zones. For complete cross-location picker, fetch all zones or iterate.
                  <optgroup key={loc.id} label={loc.name}>
                    {/* Simplified for demo: if location matches or we list zones */}
                  </optgroup>
                ))}
              </select>
            </div>
          ))}
        </div>
      </div>

      {/* Zone Add/Edit Modal */}
      {zoneModalMode && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white p-6 rounded-xl max-w-md w-full space-y-4">
            <h3 className="font-bold text-slate-900">
              {zoneModalMode === "add" ? "Add Zone" : "Edit Zone"}
            </h3>
            <div className="space-y-3">
              <div>
                <label className="text-xs font-medium text-slate-600">Zone Name</label>
                <input
                  type="text"
                  value={zoneNameInput}
                  onChange={(e) => setZoneNameInput(e.target.value)}
                  className="w-full px-3 py-1.5 text-xs rounded border border-slate-200"
                />
              </div>
              <div>
                <label className="text-xs font-medium text-slate-600">Moisture Threshold Low (0.0 - 1.0)</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  max="1"
                  value={zoneLowInput}
                  onChange={(e) => setZoneLowInput(e.target.value)}
                  className="w-full px-3 py-1.5 text-xs rounded border border-slate-200"
                />
              </div>
              <div>
                <label className="text-xs font-medium text-slate-600">Moisture Threshold High (0.0 - 1.0)</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  max="1"
                  value={zoneHighInput}
                  onChange={(e) => setZoneHighInput(e.target.value)}
                  className="w-full px-3 py-1.5 text-xs rounded border border-slate-200"
                />
              </div>
            </div>
            <div className="flex justify-end gap-2 pt-2">
              <button
                onClick={() => setZoneModalMode(null)}
                className="px-3 py-1.5 text-xs rounded border border-slate-200 text-slate-600 hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveZone}
                className="px-3 py-1.5 text-xs rounded bg-emerald-600 hover:bg-emerald-700 text-white font-semibold"
              >
                Save Zone
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}