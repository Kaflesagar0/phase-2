import { SensorList } from "../features/sensors/SensorList";
import { DeviceList } from "../components/devices/DeviceList";
import { LocationConfigWizard } from "../components/config/LocationConfigWizard";

export function DashboardPage() {
  const otherSections = [
    { id: "overview", title: "Overview", desc: "Real-time greenhouse summary & vital statistics." },
    { id: "controls", title: "Controls", desc: "Actuator states, irrigation, and ventilation." },
    { id: "config", title: "Configuration", desc: "Device setups and target environmental thresholds." },
    { id: "automation", title: "Automation", desc: "Rules and automated climate management routines." },
    { id: "events", title: "Events", desc: "System alerts, logs, and notification history." },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Greenhouse Dashboard</h1>
        <p className="text-sm text-slate-500">Monitor and manage greenhouse devices and operations.</p>
      </div>
      <section id="devices" className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs">
        <DeviceList />
      </section><section id="config" className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs lg:col-span-3">
  <LocationConfigWizard />
</section>


      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <section id="sensors" className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs">
          <SensorList />
        </section>

        {otherSections.map((sec) => (
          <section
            key={sec.id}
            id={sec.id}
            className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs flex flex-col justify-between"
          >
            <div>
              <h2 className="text-lg font-semibold text-slate-800">{sec.title}</h2>
              <p className="text-sm text-slate-500 mt-1">{sec.desc}</p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400">
              <span className="font-mono">#{sec.id}</span>
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-600">
                Coming soon
              </span>
            </div>
          </section>
        ))}
      </div>
    </div>
  );
}