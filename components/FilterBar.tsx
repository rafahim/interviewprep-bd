"use client";

import type { QuestionCategory } from "@/types";

export type BrowserFilters = { category: string; difficulty: string; topic: string; company: string; language: string; frequency: string; sort: string };
type Props = { filters: BrowserFilters; onChange: (filters: BrowserFilters) => void; categories: { id: QuestionCategory; label: string }[]; topics: string[]; companies: string[]; languages: string[] };

const selectClass = "min-w-0 rounded-xl border border-white/10 bg-[#0c1220] px-3 py-2.5 text-xs text-slate-300 outline-none transition focus:border-mint/40";

export function FilterBar({ filters, onChange, categories, topics, companies, languages }: Props) {
  function change(key: keyof BrowserFilters, value: string) { onChange({ ...filters, [key]: value }); }
  return <div className="panel p-3 sm:p-4">
    <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-7">
      <select aria-label="Category" className={selectClass} value={filters.category} onChange={(event) => change("category", event.target.value)}><option value="">All categories</option>{categories.map((item) => <option key={item.id} value={item.id}>{item.label}</option>)}</select>
      <select aria-label="Difficulty" className={selectClass} value={filters.difficulty} onChange={(event) => change("difficulty", event.target.value)}><option value="">All difficulty</option><option>Easy</option><option>Medium</option><option>Hard</option></select>
      <select aria-label="Topic" className={selectClass} value={filters.topic} onChange={(event) => change("topic", event.target.value)}><option value="">All topics</option>{topics.map((value) => <option key={value}>{value}</option>)}</select>
      <select aria-label="Company" className={selectClass} value={filters.company} onChange={(event) => change("company", event.target.value)}><option value="">All companies</option>{companies.map((value) => <option key={value}>{value}</option>)}</select>
      <select aria-label="Language" className={selectClass} value={filters.language} onChange={(event) => change("language", event.target.value)}><option value="">All languages</option>{languages.map((value) => <option key={value}>{value}</option>)}</select>
      <select aria-label="Frequency" className={selectClass} value={filters.frequency} onChange={(event) => change("frequency", event.target.value)}><option value="">All frequency</option><option>High</option><option>Medium</option><option>Low</option></select>
      <select aria-label="Sort questions" className={selectClass} value={filters.sort} onChange={(event) => change("sort", event.target.value)}><option value="recommended">Recommended</option><option value="title">Title A–Z</option><option value="difficulty">Difficulty</option><option value="time">Time needed</option><option value="frequency">Frequency</option></select>
    </div>
    <div className="mt-3 flex justify-end"><button onClick={() => onChange({ category: "", difficulty: "", topic: "", company: "", language: "", frequency: "", sort: "recommended" })} className="text-xs text-slate-500 transition hover:text-mint">Reset filters ↺</button></div>
  </div>;
}
