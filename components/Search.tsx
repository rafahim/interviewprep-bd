"use client";

import Fuse from "fuse.js";
import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import type { QuestionIndexItem } from "@/types";

export function Search() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [questions, setQuestions] = useState<QuestionIndexItem[]>([]);
  const [loading, setLoading] = useState(false);
  const openSearch = useCallback(() => setOpen(true), []);

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        openSearch();
      }
      if (event.key === "Escape") setOpen(false);
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [openSearch]);

  useEffect(() => {
    if (!open || questions.length) return;
    setLoading(true);
    fetch("/interview-prep/api/questions/")
      .then((response) => response.ok ? response.json() : [])
      .then((data: QuestionIndexItem[]) => setQuestions(Array.isArray(data) ? data : []))
      .catch(() => setQuestions([]))
      .finally(() => setLoading(false));
  }, [open, questions.length]);

  const fuse = useMemo(() => new Fuse(questions, {
    keys: ["title", "topic", "problem", "tags", "companies", "category"],
    threshold: 0.36,
    ignoreLocation: true
  }), [questions]);
  const results = useMemo(() => {
    if (!query.trim()) return questions.slice(0, 6);
    return fuse.search(query.trim(), { limit: 8 }).map((item) => item.item);
  }, [fuse, query, questions]);

  return <>
    <button onClick={openSearch} className="flex items-center gap-2 rounded-xl border border-white/10 bg-white/[0.035] px-3 py-2 text-xs text-slate-400 transition hover:border-mint/40 hover:text-white" aria-label="Search questions">
      <span aria-hidden="true">⌕</span><span className="hidden sm:inline">Search</span><kbd className="hidden rounded border border-white/10 px-1.5 py-0.5 font-mono text-[10px] sm:inline">⌘K</kbd>
    </button>
    {open && <div className="fixed inset-0 z-[70] flex items-start justify-center bg-black/70 px-4 pt-[12vh] backdrop-blur-sm" onMouseDown={(event) => { if (event.target === event.currentTarget) setOpen(false); }}>
      <section className="w-full max-w-2xl overflow-hidden rounded-2xl border border-white/10 bg-[#0c1220] shadow-2xl" role="dialog" aria-modal="true" aria-label="Search interview questions">
        <div className="flex items-center gap-3 border-b border-white/10 px-4">
          <span className="text-xl text-mint">⌕</span>
          <input autoFocus value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search questions, topics, companies…" className="w-full bg-transparent py-4 text-sm text-white outline-none placeholder:text-slate-500" />
          <button onClick={() => setOpen(false)} className="rounded-md border border-white/10 px-2 py-1 text-[10px] text-slate-400">ESC</button>
        </div>
        <div className="max-h-[52vh] overflow-y-auto p-2">
          {loading && <p className="px-3 py-6 text-sm text-slate-500">Loading question index…</p>}
          {!loading && results.length === 0 && <p className="px-3 py-6 text-sm text-slate-500">No matching question. অন্য keyword দিয়ে চেষ্টা করো।</p>}
          {results.map((item) => <Link key={item.slug} onClick={() => setOpen(false)} href={`/questions/${item.slug}/`} className="flex items-center justify-between gap-3 rounded-xl px-3 py-3 transition hover:bg-white/[0.06]">
            <span className="min-w-0"><span className="block truncate text-sm font-semibold text-slate-100">{item.title}</span><span className="mt-1 block truncate text-xs text-slate-500">{item.topic} · {item.difficulty}</span></span>
            <span className="shrink-0 text-slate-600">↗</span>
          </Link>)}
        </div>
        <div className="flex items-center justify-between border-t border-white/10 px-4 py-2.5 text-[10px] text-slate-600"><span>বাংলা + English · {questions.length || "…"} questions</span><span>ESC to close</span></div>
      </section>
    </div>}
  </>;
}
