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

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/health`);
  if (!response.ok) {
    throw new Error(`Failed to fetch health status: ${response.statusText}`);
  }
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