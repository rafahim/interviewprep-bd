"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import type { QuestionIndexItem, ProgressMap, ProgressStatus } from "@/types";
import { ProgressChart } from "@/components/ProgressChart";
import { formatDate } from "@/lib/utils";
import { getCurrentStreak, readActivity, readProgress, saveStatus } from "@/lib/progress";

const statusOptions: { value: ProgressStatus; label: string; color: string }[] = [
  { value: "todo", label: "To do", color: "bg-slate-400" },
  { value: "in-progress", label: "In progress", color: "bg-sky-400" },
  { value: "solved", label: "Solved", color: "bg-emerald-400" },
  { value: "needs-review", label: "Needs review", color: "bg-amber-300" }
];

export function ProgressDashboard({ questions }: { questions: QuestionIndexItem[] }) {
  const [progress, setProgress] = useState<ProgressMap>({});
  const [activity, setActivity] = useState<string[]>([]);
  const [filter, setFilter] = useState<ProgressStatus | "all" | "due">("all");
  const [search, setSearch] = useState("");
  const [revision, setRevision] = useState(0);
  useEffect(() => { setProgress(readProgress()); setActivity(readActivity()); }, [revision]);
  const counts = useMemo(() => {
    const result: Record<ProgressStatus, number> = { todo: 0, "in-progress": 0, solved: 0, "needs-review": 0 };
    for (const question of questions) result[progress[question.slug]?.status || "todo"] += 1;
    return result;
  }, [progress, questions]);
  const dueCount = useMemo(() => questions.filter((question) => {
    const due = progress[question.slug]?.nextReview;
    return !due || new Date(due).getTime() <= Date.now();
  }).length, [progress, questions]);
  const filtered = useMemo(() => questions.filter((question) => {
    const status = progress[question.slug]?.status || "todo";
    const due = progress[question.slug]?.nextReview;
    const statusMatch = filter === "all" || filter === status || (filter === "due" && (!due || new Date(due).getTime() <= Date.now()));
    return statusMatch && `${question.title} ${question.topic}`.toLowerCase().includes(search.toLowerCase());
  }).slice(0, 30), [filter, progress, questions, search]);
  const chart = statusOptions.map((option) => ({ label: option.label, value: counts[option.value], color: option.color }));
  const streak = getCurrentStreak(activity);
  function update(slug: string, status: ProgressStatus) { saveStatus(slug, status); setRevision((value) => value + 1); }

  return <div className="space-y-6">
    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">{[{ label: "Solved", value: counts.solved, note: `${Math.round(counts.solved / Math.max(1, questions.length) * 100)}% of library`, color: "text-mint" }, { label: "In progress", value: counts["in-progress"], note: "Currently working on", color: "text-sky" }, { label: "Due to review", value: dueCount, note: "Spaced repetition queue", color: "text-amber" }, { label: "Day streak", value: streak, note: "Study days in a row", color: "text-white" }].map((item) => <div key={item.label} className="panel p-5"><p className="text-xs text-slate-500">{item.label}</p><p className={`mt-2 text-3xl font-bold tabular-nums ${item.color}`}>{item.value}</p><p className="mt-2 text-xs text-slate-600">{item.note}</p></div>)}</div>
    <div className="grid gap-5 lg:grid-cols-[0.8fr_1.2fr]"><ProgressChart data={chart} total={questions.length} /><div className="panel p-5"><div className="flex items-center justify-between gap-3"><h3 className="font-semibold text-slate-100">Study activity</h3><span className="text-xs text-slate-500">Last 14 days</span></div><div className="mt-5 grid grid-cols-7 gap-2 sm:grid-cols-14">{Array.from({ length: 14 }, (_, index) => { const day = new Date(); day.setDate(day.getDate() - (13 - index)); const key = day.toISOString().slice(0, 10); const active = activity.includes(key); return <div key={key} className="text-center"><div title={`${key}${active ? " · studied" : " · no activity"}`} className={`mx-auto aspect-square w-full max-w-8 rounded-md border ${active ? "border-mint/20 bg-mint/70" : "border-white/[0.05] bg-white/[0.035]"}`} /><span className="mt-2 block text-[9px] text-slate-600">{day.getDate()}</span></div>; })}</div><p className="mt-4 text-xs leading-5 text-slate-500">কোনো question পড়া, bookmark করা, note save বা review rate করলে activity record হয়। Data শুধু এই browser-এ রাখা হয়।</p></div></div>
    <div className="panel p-5"><div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between"><div><h3 className="text-lg font-semibold text-white">Question tracker</h3><p className="mt-1 text-xs text-slate-500">Status এবং review schedule এই device-এ save হয়।</p></div><label className="text-xs text-slate-500">Find a question<input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search title or topic" className="mt-2 block w-full rounded-xl border border-white/10 bg-[#0b101c] px-3 py-2.5 text-sm text-slate-200 outline-none sm:w-56" /></label></div>
      <div className="mt-4 flex flex-wrap gap-2">{[{ value: "all", label: "All" }, ...statusOptions.map((item) => ({ value: item.value, label: item.label })), { value: "due", label: "Due for review" }].map((item) => <button key={item.value} onClick={() => setFilter(item.value as typeof filter)} className={`rounded-lg border px-3 py-2 text-xs font-semibold ${filter === item.value ? "border-mint/30 bg-mint/10 text-mint" : "border-white/10 text-slate-500 hover:text-slate-200"}`}>{item.label}</button>)}</div>
      <div className="mt-4 divide-y divide-white/[0.06]">{filtered.map((question) => { const record = progress[question.slug]; const status = record?.status || "todo"; return <div key={question.slug} className="flex flex-col gap-3 py-3 sm:flex-row sm:items-center sm:justify-between"><div className="min-w-0"><Link href={`/questions/${question.slug}/`} className="text-sm font-semibold text-slate-200 hover:text-mint">{question.title}</Link><p className="mt-1 text-xs text-slate-600">{question.topic} · Next review: {formatDate(record?.nextReview || null)}</p></div><select aria-label={`Status for ${question.title}`} value={status} onChange={(event) => update(question.slug, event.target.value as ProgressStatus)} className="rounded-lg border border-white/10 bg-[#0b101c] px-3 py-2 text-xs text-slate-300"><option value="todo">To do</option><option value="in-progress">In progress</option><option value="solved">Solved</option><option value="needs-review">Needs review</option></select></div>; })}</div>
      {filtered.length === 0 && <p className="py-8 text-center text-sm text-slate-500">No matching questions.</p>}
      {questions.length > filtered.length && <p className="mt-3 text-center text-[11px] text-slate-600">Showing up to 30 matches. Use search to narrow the list.</p>}
    </div>
  </div>;
}
