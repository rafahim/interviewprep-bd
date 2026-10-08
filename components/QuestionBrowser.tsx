"use client";

import Fuse from "fuse.js";
import { useMemo, useState } from "react";
import type { QuestionCategory, QuestionIndexItem } from "@/types";
import { CATEGORY_LABELS, CATEGORY_ORDER } from "@/lib/categories";
import { FilterBar, type BrowserFilters } from "@/components/FilterBar";
import { QuestionCard } from "@/components/QuestionCard";

const initialFilters: BrowserFilters = { category: "", difficulty: "", topic: "", company: "", language: "", frequency: "", sort: "recommended" };
const difficultyOrder: Record<string, number> = { Easy: 1, Medium: 2, Hard: 3 };

export function QuestionBrowser({ questions, initialCategory = "" }: { questions: QuestionIndexItem[]; initialCategory?: string }) {
  const [query, setQuery] = useState("");
  const [filters, setFilters] = useState<BrowserFilters>({ ...initialFilters, category: initialCategory });
  const fuse = useMemo(() => new Fuse(questions, { keys: ["title", "problem", "topic", "tags", "companies", "category"], threshold: 0.38, ignoreLocation: true }), [questions]);
  const topics = useMemo(() => [...new Set(questions.map((question) => question.topic))].sort(), [questions]);
  const companies = useMemo(() => [...new Set(questions.flatMap((question) => question.companies))].sort(), [questions]);
  const languages = useMemo(() => [...new Set(questions.flatMap((question) => question.languages))].sort(), [questions]);
  const filtered = useMemo(() => {
    const source = query.trim() ? fuse.search(query.trim()).map((result) => result.item) : questions;
    const result = source.filter((question) => (!filters.category || question.category === filters.category) && (!filters.difficulty || question.difficulty === filters.difficulty) && (!filters.topic || question.topic === filters.topic) && (!filters.company || question.companies.includes(filters.company)) && (!filters.language || question.languages.includes(filters.language)) && (!filters.frequency || question.frequency === filters.frequency));
    if (filters.sort === "title") result.sort((a, b) => a.title.localeCompare(b.title));
    if (filters.sort === "difficulty") result.sort((a, b) => difficultyOrder[a.difficulty] - difficultyOrder[b.difficulty] || a.title.localeCompare(b.title));
    if (filters.sort === "time") result.sort((a, b) => a.minutes - b.minutes);
    if (filters.sort === "frequency") result.sort((a, b) => ["High", "Medium", "Low"].indexOf(a.frequency) - ["High", "Medium", "Low"].indexOf(b.frequency));
    return result;
  }, [filters, fuse, questions, query]);
  const categories = CATEGORY_ORDER.map((id: QuestionCategory) => ({ id, label: CATEGORY_LABELS[id] }));
  return <div className="space-y-5">
    <div className="flex flex-col gap-3 sm:flex-row"><label className="relative flex-1"><span className="sr-only">Search questions</span><span className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-slate-500">⌕</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search by question, concept, company…" className="w-full rounded-xl border border-white/10 bg-white/[0.035] py-3 pl-11 pr-4 text-sm text-white outline-none placeholder:text-slate-600 focus:border-mint/40" /></label><div className="flex items-center justify-between rounded-xl border border-white/10 px-4 py-3 text-xs text-slate-400 sm:min-w-40"><span>Matching questions</span><strong className="text-mint">{filtered.length} / {questions.length}</strong></div></div>
    <FilterBar filters={filters} onChange={setFilters} categories={categories} topics={topics} companies={companies} languages={languages} />
    {filtered.length ? <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">{filtered.map((question, index) => <QuestionCard key={question.slug} question={question} index={index + 1} />)}</div> : <div className="panel px-6 py-16 text-center"><p className="text-lg font-semibold text-slate-200">No questions found</p><p className="mt-2 text-sm text-slate-500">Search term বা filter পরিবর্তন করে আবার চেষ্টা করো।</p><button onClick={() => { setQuery(""); setFilters(initialFilters); }} className="mt-5 rounded-xl bg-mint px-4 py-2.5 text-sm font-bold text-ink">Clear filters</button></div>}
  </div>;
}
