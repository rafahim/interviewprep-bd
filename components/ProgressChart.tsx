type Segment = { label: string; value: number; color: string };

export function ProgressChart({ data, total }: { data: Segment[]; total: number }) {
  return <div className="panel p-5"><div className="flex items-center justify-between"><h3 className="font-semibold text-slate-100">Progress overview</h3><span className="text-xs text-slate-500">{total} questions</span></div><div className="mt-5 space-y-4">{data.map((item) => <div key={item.label}><div className="mb-2 flex items-center justify-between text-xs"><span className="text-slate-400">{item.label}</span><span className="font-mono text-slate-300">{item.value} <span className="text-slate-600">/ {total}</span></span></div><div className="h-2 overflow-hidden rounded-full bg-white/[0.05]"><div className={`h-full rounded-full ${item.color}`} style={{ width: `${total ? Math.min(100, (item.value / total) * 100) : 0}%` }} /></div></div>)}</div></div>;
}
