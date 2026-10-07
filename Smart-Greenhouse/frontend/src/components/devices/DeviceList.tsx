import { useEffect, useState, useCallback } from "react";
import { fetchDevices, provisionFamily, type DeviceDto } from "../../services/api";
import { DeviceFamilySwitcher } from "./DeviceFamilySwitcher";

export function DeviceList() {
    const [family, setFamily] = useState<string>("simulation");
    const [devices, setDevices] = useState<DeviceDto[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [provisioning, setProvisioning] = useState(false);

    const loadDevices = useCallback(async (targetFamily: string) => {
        try {
            setLoading(true);
            setError(null);
            const data = await fetchDevices(targetFamily);
            setDevices(data);
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : "Failed to load devices");
        } finally  { 
            setLoading(false);
        }
        }, []);

        useEffect(() => {
            loadDevices(family);
        }, [family, loadDevices]);
    
       const handleProvision = async () => {
        try {
            setProvisioning(true),
            setError(null);
            await provisionFamily(family);
            await loadDevices(family);
        } catch (err: unknown ) {
            setError(err instanceof Error ? err.message : "Provisioning failed");
        } finally {
            setProvisioning(false);

        }
        };

        return (
            <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4" >
                    <div>
                        <h2 className="text-lg font-semibold text-slate-800">Unified Devices</h2>
                        <p className="text-xs text-slate-500">Coherent device kits managed by Abstract Factory</p>
                    
                    </div>
                    <div className="flex items-center gap-3">
                        <DeviceFamilySwitcher selectedFamily={family} onSelectFamily={setFamily} />
                        <button
                           onClick={handleProvision}
                           disabled={provisioning}
                          className="px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 disabled:opacity-50 transition-colors shadow-xs"
             >
                          {provisioning ? "Provisioning..." : `+ Provision ${family} Kit`}
                        </button>
                    </div>


                </div>

                {error && (
                   <div className="p-3 text-xs rounded-lg bg-red-50 text-red-700 border border-red-200">
                      {error}
                    </div>
                )}

                {loading ? (
                   <p className="text-xs text-slate-400 py-6 text-center">Loading devices...</p>
               ) : devices.length === 0 ? (
                 <div className="text-center py-8 border border-dashed border-slate-200 rounded-xl bg-slate-50/50">
                    <p className="text-xs text-slate-500 font-medium">No devices found for the '{family}' family.</p>
                     <p className="text-[11px] text-slate-400 mt-1">Click the provision button above to create a device kit.</p>
                 </div>
               ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-96 overflow-y-auto pr-1">
                   {devices.map((d) => (
                      <div key={d.id} className="p-3.5 rounded-xl border border-slate-200 bg-white text-xs flex flex-col justify-between gap-2 shadow-xs">
                         <div className="flex justify-between items-start">
                          <div>
                            <span className="font-semibold text-slate-800 block text-sm">{d.display_name}</span>
                             <span className="font-mono text-[10px] text-slate-400">{d.device_type}</span>
                          </div>
                          <div className="flex items-center gap-1.5">
                              <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold uppercase ${
                                 d.role === "sensor" ? "bg-blue-50 text-blue-700 border border-blue-200" : "bg-purple-50 text-purple-700 border border-purple-200"
                              }`}>
                                {d.role}
                              </span>
                             <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold uppercase bg-slate-100 text-slate-600 border border-slate-200">
                              {d.device_family}
                             </span>
                          </div>
                         </div>
                         <pre className="text-[10px] text-slate-600 bg-slate-50 p-2 rounded-md border border-slate-100 overflow-x-auto">
                            {JSON.stringify(d.default_config, null, 2)}
                         </pre>
                     </div>
                   ))}
                </div>
              )}
            </div>
        );

    }
       
        
        
    
