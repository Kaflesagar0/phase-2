interface DeviceFamilySwitcherProps {
    selectedFamily: string; 
    onSelectFamily: (family: string) => void;
}

export function DeviceFamilySwitcher({ selectedFamily, onSelectFamily }: DeviceFamilySwitcherProps) {
    const families = ["simulation", "edge"];

    return ( 
        <div className="flex items-center gap-2">
            <span className="text-xs font-medium text-slate-500">Family:</span>
            <div className="inline-flex rounded-lg bg-slate-100 p-1 border border-slate-200">
                {families.map((family) => {
                    const isActive = selectedFamily === family;
                    return (
                        <button 
                        key={family}
                        onClick={() => onSelectFamily(family)}
                        className={`px-3 py-1 text-xs font-semibold rounded-lg capitalize transition-all ${
                           isActive ? "bg-white text-emerald-700 shadow-xs border border-slate-200/60" 
                           : "text-slate-600 hover:text-slate-900"
                        }`}
                        >
                            {family}
                        </button>
                    );
                })}
            </div>
        </div>
    );
}