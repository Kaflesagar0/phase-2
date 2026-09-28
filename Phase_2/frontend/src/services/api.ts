//export interface HealthResponse {
  //status: string;
  //db: "ok" | "fail";
//}

export interface DeviceDto {
  id: string;
  device_type: string;
  role: "sensor" | "actuator";
  device_family: string;
  display_name: string;
  default_config: Record<string, unknown>;
}
//export interface SensorDto {
 // id: string;
 // device_type: string;
//  display_name: string;
 // default_config: Record<string, unknown>;
//}

//export interface CreateSensorPayload {
 //: string;
 // display_name?: string | null;
//}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function fetchDevices(family?: string, role?:string): Promise<DeviceDto[]> {
  const params = new URLSearchParams();
  if (family) params.append("family", family);
  if (role) params.append("role", role);

  const query = params.toString() ? `?${params.toString()}`: "";
  const response = await fetch(`${API_BASE_URL}/api/devices${query}`); 
  if (!response.ok) {
    throw new Error("Failed to fetch devices");

  }
  return response.json();
}

export async function provisionFamily(family: string): Promise<DeviceDto[]> {
  const response = await fetch(`${API_BASE_URL}/api/devices/provision?family=${encodeURIComponent(family)}`, {
    method: "POST",
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: "Failed to provision family" }));
     throw new Error(errorData.detail || "Failed to provision family");
  }
  return response.json();
}


//export async function fetchHealth(): Promise<HealthResponse> {
//  const response = await fetch(`${API_BASE_URL}/health`);
 // if (!response.ok) {
  //  throw new Error(`Failed to fetch health status: ${response.statusText}`);
 // }
 // return response.json();
//}

//export async function fetchSensors(): Promise<SensorDto[]> {
  //const response = await fetch(`${API_BASE_URL}/api/sensors`);
 // if (!response.ok) throw new Error("Failed to fetch sensors");
  //return response.json();

//}

//export async function createSensor(payload: CreateSensorPayload): Promise<SensorDto> {
  //const response = await fetch(`${API_BASE_URL}/api/sensors`, {
   // method: "POST",
   // headers: { "Content-Type": "application/json" },
    //body: JSON.stringify(payload),
  //});
  //if (!response.ok) {
  //  const errorData = await response.json().catch(() => ({ detail: "Failed to create sensor" }));
   // throw new Error(errorData.detail || "Failed to create sensor");
 // }
  //return response.json();
//}