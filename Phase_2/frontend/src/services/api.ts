

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// --- Types & DTOs ---

export interface HealthResponse {
  status: string;
  db: "ok" | "fail";
}

export interface SensorDto {
  id: string;
  device_type: string;
  display_name: string;
  default_config: Record<string, unknown>;
}

export interface CreateSensorPayload {
  type: string;
  display_name?: string | null;
}

export interface DeviceDto {
  id: string;
  device_type: string;
  role: string;
  device_family: string;
  display_name: string;
  default_config: Record<string, unknown>;
  zone_id?: string | null;
  location_id?: string | null;
}

export interface ZoneDto {
  id: string;
  location_id: string;
  name: string;
  moisture_threshold_low: number;
  moisture_threshold_high: number;
  schedule: Record<string, unknown>;
}

export interface LocationMetadataDto {
  id: string;
  name: string;
}

export interface LocationConfigDto {
  location: LocationMetadataDto;
  zones: ZoneDto[];
}

export interface ZoneDeviceDto {
  id: string;
  device_type: string;
  role: string;
  display_name: string | null;
  zone_id: string | null;
  location_id: string | null;
}

export interface ReadingDto{
  id: string;
  device_id: string;
  value: number;
  unit: string;
  source: string;
  recorded_at: string;
}

// --- API Functions ---

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) throw new Error("Failed to fetch health status");
  return response.json();
}

export async function fetchSensors(): Promise<SensorDto[]> {
  const response = await fetch(`${API_BASE_URL}/api/sensors`);
  if (!response.ok) throw new Error("Failed to fetch sensors");
  return response.json();
}

export async function createSensor(payload: CreateSensorPayload): Promise<SensorDto> {
  const response = await fetch(`${API_BASE_URL}/api/sensors`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: "Failed to create sensor" }));
    throw new Error(errorData.detail || "Failed to create sensor");
  }
  return response.json();
}

export async function fetchDevices(family?: string, role?: string): Promise<DeviceDto[]> {
  let url = `${API_BASE_URL}/api/devices`;
  const params = new URLSearchParams();
  if (family) params.append("family", family);
  if (role) params.append("role", role);
  if (params.toString()) url += `?${params.toString()}`;

  const response = await fetch(url);
  if (!response.ok) throw new Error("Failed to fetch devices");
  return response.json();
}

export async function provisionFamily(family: string): Promise<DeviceDto[]> {
  const response = await fetch(`${API_BASE_URL}/api/devices/provision?family=${encodeURIComponent(family)}`, {
    method: "POST",
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: "Failed to provision family" }));
    throw new Error(err.detail || "Failed to provision family");
  }
  return response.json();
} 

export async function provisionDevices(family: string): Promise<DeviceDto[]> {
  const response = await fetch(`${API_BASE_URL}/api/devices/provision?family=${encodeURIComponent(family)}`, {
    method: "POST",
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: "Failed to provision devices" }));
    throw new Error(err.detail || "Failed to provision devices");
  }
  return response.json();
}

// --- Phase 4: Locations & Zones API ---

export async function fetchLocations(): Promise<LocationMetadataDto[]> {
  const res = await fetch(`${API_BASE_URL}/api/locations`);
  if (!res.ok) throw new Error("Failed to fetch locations");
  return res.json();
}

export async function fetchLocationConfig(locationId: string): Promise<LocationConfigDto> {
  const res = await fetch(`${API_BASE_URL}/api/locations/${locationId}/config`);
  if (!res.ok) throw new Error("Failed to fetch location configuration");
  return res.json();
}

export async function createLocationConfig(payload: {
  location_name: string;
  zones: Array<{
    name: string;
    moisture_threshold_low: number;
    moisture_threshold_high: number;
    schedule?: Record<string, unknown>;
  }>;
}): Promise<LocationConfigDto> {
  const res = await fetch(`${API_BASE_URL}/api/locations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Failed to create location" }));
    throw new Error(err.detail || "Failed to create location");
  }
  return res.json();
}

export async function deleteLocation(locationId: string): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/api/locations/${locationId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete location");
}

export async function addZone(locationId: string, payload: {
  name: string;
  moisture_threshold_low: number;
  moisture_threshold_high: number;
  schedule?: Record<string, unknown>;
}): Promise<ZoneDto> {
  const res = await fetch(`${API_BASE_URL}/api/locations/${locationId}/zones`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Failed to add zone" }));
    throw new Error(err.detail || "Failed to add zone");
  }
  return res.json();
}

export async function editZone(locationId: string, zoneId: string, payload: {
  name: string;
  moisture_threshold_low: number;
  moisture_threshold_high: number;
  schedule?: Record<string, unknown>;
}): Promise<ZoneDto> {
  const res = await fetch(`${API_BASE_URL}/api/locations/${locationId}/zones/${zoneId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Failed to update zone" }));
    throw new Error(err.detail || "Failed to update zone");
  }
  return res.json();
}

export async function deleteZone(locationId: string, zoneId: string): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/api/locations/${locationId}/zones/${zoneId}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Failed to delete zone" }));
    throw new Error(err.detail || "Failed to delete zone");
  }
}

export async function assignDeviceZone(deviceId: string, zoneId: string | null): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/api/devices/${deviceId}/zone`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ zone_id: zoneId }),
  });
  if (!res.ok) throw new Error("Failed to assign device zone");
}

export async function triggerSensorRead(deviceId: string, useVendor: boolean = false): Promise<ReadingDto> {
  const response = await fetch(`${API_BASE_URL}/api/sensors/${deviceId}/read?use_vendor=${useVendor}`, {
    method: "POST",
  });
  if (!response.ok)  {
    const errorData = await response.json().catch(() => ({ detail: "Failed to trigger sensor read"}));
    throw new Error(errorData.detail || "Failed to trigger sensor read");

  }
  return response.json();
}

export async function fetchSensorReadings(deviceId: string, limit: number = 1): Promise<ReadingDto[]> {
  const response = await fetch(`${API_BASE_URL}/api/sensors/${deviceId}/readings?limit=${limit}`);
  if (!response.ok) {
    throw new Error("Failed to fetch sensor readings");

  }
  return response.json();
}

export async function updateDeviceSampling(
  deviceId: string,
  samplingIntervalSeconds: number,
  trackingEnabled: boolean
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/devices/${deviceId}/sampling`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json"},
    body: JSON.stringify({
      sampling_interval_seconds: samplingIntervalSeconds,
      tracking_enabled: trackingEnabled,
    }),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({detail: "Failed to update sampling settings."}));
    throw new Error(errorData.detail || "Failed to update sampling settings");
  }
}