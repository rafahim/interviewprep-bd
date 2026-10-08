"use client";

import { useEffect, useState } from "react";

function clock(seconds: number) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, "0");
  const remaining = (seconds % 60).toString().padStart(2, "0");
  return `${minutes}:${remaining}`;
}

export function Timer({ initialMinutes = 30 }: { initialMinutes?: number }) {
  const [duration, setDuration] = useState(initialMinutes * 60);
  const [remaining, setRemaining] = useState(initialMinutes * 60);
  const [running, setRunning] = useState(false);
  useEffect(() => {
    if (!running || remaining <= 0) return;
    const id = window.setInterval(() => setRemaining((value) => Math.max(0, value - 1)), 1000);
    return () => window.clearInterval(id);
  }, [running, remaining]);
  useEffect(() => { if (remaining === 0) setRunning(false); }, [remaining]);
  function reset() { setRunning(false); setRemaining(duration); }
  return <div className="panel flex flex-wrap items-center justify-between gap-4 p-4">
    <div><p className="text-[10px] font-bold uppercase tracking-[0.16em] text-slate-500">Mock interview timer</p><p className={`mt-1 font-mono text-3xl font-bold tabular-nums ${remaining <= 60 ? "text-rose-300" : "text-white"}`}>{clock(remaining)}</p></div>
    <div className="flex flex-wrap items-center gap-2"><select aria-label="Timer duration" value={duration / 60} onChange={(event) => { const next = Number(event.target.value) * 60; setDuration(next); setRemaining(next); setRunning(false); }} className="rounded-lg border border-white/10 bg-[#0c1220] px-2.5 py-2 text-xs text-slate-300"><option value="15">15 min</option><option value="30">30 min</option><option value="45">45 min</option><option value="60">60 min</option></select><button onClick={() => remaining > 0 && setRunning((value) => !value)} className="rounded-lg bg-mint px-3 py-2 text-xs font-bold text-ink">{running ? "Pause" : "Start"}</button><button onClick={reset} className="rounded-lg border border-white/10 px-3 py-2 text-xs text-slate-300">Reset</button></div>
  </div>;
}
