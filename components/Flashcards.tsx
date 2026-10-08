"use client";

import { useMemo, useState } from "react";
import type { QuestionIndexItem } from "@/types";
import { readProgress, reviewQuestion } from "@/lib/progress";

export function Flashcards({ questions }: { questions: QuestionIndexItem[] }) {
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [filter, setFilter] = useState("due");
  const [revision, setRevision] = useState(0);
  const cards = useMemo(() => {
    const progress = readProgress();
    const now = Date.now();
    const sorted = [...questions].sort((a, b) => a.title.localeCompare(b.title));
    if (filter === "all") return sorted;
    if (filter === "bookmarked") {
      let bookmarks: string[] = [];
      try { bookmarks = JSON.parse(window.localStorage.getItem("ipbd.bookmarks.v1") || "[]") as string[]; } catch { bookmarks = []; }
      return sorted.filter((question) => bookmarks.includes(question.slug));
    }
    return sorted.filter((question) => {
      const item = progress[question.slug];
      if (!item || !item.nextReview) return true;
      return new Date(item.nextReview).getTime() <= now;
    });
  }, [filter, questions, revision]);
  const current = cards.length ? cards[index % cards.length] : null;

  function move(direction: number) {
    setIndex((value) => cards.length ? (value + direction + cards.length) % cards.length : 0);
    setFlipped(false);
  }

  function rate(value: number) {
    if (!current) return;
    reviewQuestion(current.slug, value);
    setRevision((previous) => previous + 1);
    setFlipped(false);
    setIndex((previous) => cards.length ? (previous + 1) % cards.length : 0);
  }

  return <div className="mx-auto max-w-4xl space-y-6">
    <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-[0.18em] text-mint">Recall practice</p><h2 className="mt-2 text-3xl font-bold tracking-tight text-white">Flashcards</h2><p className="mt-2 text-sm text-slate-400">প্রশ্ন থেকে card স্বয়ংক্রিয়ভাবে তৈরি হয়েছে। আগে উত্তর মনে করার চেষ্টা করো, তারপর reveal করো।</p></div><label className="text-xs text-slate-500">Card set<select value={filter} onChange={(event) => { setFilter(event.target.value); setIndex(0); setFlipped(false); }} className="mt-2 block rounded-xl border border-white/10 bg-[#0c1220] px-3 py-2.5 text-sm text-slate-200"><option value="due">Due for review</option><option value="all">All flashcards</option><option value="bookmarked">Bookmarked</option></select></label></div>
    {current ? <><div className="flex items-center justify-between text-xs text-slate-500"><span>Card {index + 1} of {cards.length}</span><span>{current.topic} · {current.difficulty}</span></div><button onClick={() => setFlipped((value) => !value)} className="soft-grid panel flex min-h-[340px] w-full flex-col items-center justify-center p-8 text-center transition hover:border-mint/30 sm:min-h-[390px]" aria-label="Flip flashcard"><span className="rounded-full border border-mint/20 bg-mint/10 px-3 py-1 text-[10px] font-bold uppercase tracking-[0.16em] text-mint">{flipped ? "Answer" : "Recall"}</span><span className="mt-8 max-w-2xl text-2xl font-semibold leading-relaxed text-white sm:text-3xl">{flipped ? current.back : current.front}</span><span className="mt-8 text-xs text-slate-600">{flipped ? "Click to see the prompt" : "Click to reveal answer"}</span></button><div className="flex flex-wrap justify-center gap-2"><button onClick={() => move(-1)} className="rounded-xl border border-white/10 px-4 py-3 text-sm text-slate-300">← Previous</button><button onClick={() => setFlipped((value) => !value)} className="rounded-xl bg-mint px-5 py-3 text-sm font-bold text-ink">{flipped ? "Show prompt" : "Reveal answer"}</button><button onClick={() => move(1)} className="rounded-xl border border-white/10 px-4 py-3 text-sm text-slate-300">Next →</button></div>{flipped && <div className="panel p-5"><p className="text-center text-sm font-semibold text-slate-200">How well did you recall it?</p><div className="mt-4 grid grid-cols-3 gap-2"><button onClick={() => rate(1)} className="rounded-xl border border-rose-400/20 bg-rose-400/[0.05] px-3 py-3 text-xs font-semibold text-rose-200">Again · 1 day</button><button onClick={() => rate(3)} className="rounded-xl border border-amber/20 bg-amber/[0.05] px-3 py-3 text-xs font-semibold text-amber-100">Good · spaced</button><button onClick={() => rate(5)} className="rounded-xl border border-mint/20 bg-mint/[0.05] px-3 py-3 text-xs font-semibold text-mint">Easy · spaced</button></div><p className="mt-3 text-center text-[11px] text-slate-500">SM-2 interval ও next review date এই device-এ save হয়।</p></div>}</> : <div className="panel p-12 text-center"><h3 className="text-lg font-semibold text-white">No cards in this set</h3><p className="mt-2 text-sm text-slate-500">সব question দেখো অথবা কিছু question bookmark করে এই set-এ ফিরো।</p><button onClick={() => setFilter("all")} className="mt-5 rounded-xl bg-mint px-4 py-2.5 text-sm font-bold text-ink">Show all cards</button></div>}
  </div>;
}
