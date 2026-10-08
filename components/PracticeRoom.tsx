"use client";

import { useMemo, useState } from "react";
import type { QuestionIndexItem } from "@/types";
import { QuestionCard } from "@/components/QuestionCard";
import { Timer } from "@/components/Timer";
import { recordActivity, reviewQuestion } from "@/lib/progress";

export function PracticeRoom({ questions }: { questions: QuestionIndexItem[] }) {
  const [category, setCategory] = useState("all");
  const [difficulty, setDifficulty] = useState("all");
  const [current, setCurrent] = useState<QuestionIndexItem | null>(null);
  const [notes, setNotes] = useState("");
  const [savedNotes, setSavedNotes] = useState("");
  const [rating, setRating] = useState(3);
  const [mode, setMode] = useState("random");
  const [session, setSession] = useState<QuestionIndexItem[]>([]);
  const pool = useMemo(() => questions.filter((question) => (category === "all" || question.category === category) && (difficulty === "all" || question.difficulty === difficulty)), [category, difficulty, questions]);

  function chooseQuestion() {
    if (!pool.length) return;
    const item = pool[Math.floor(Math.random() * pool.length)];
    setCurrent(item);
    setNotes("");
    setSavedNotes("");
    setSession((previous) => [...previous.filter((entry) => entry.slug !== item.slug), item].slice(-10));
    recordActivity();
  }

  function startMock() {
    const shuffled = [...pool].sort(() => Math.random() - 0.5).slice(0, Math.min(5, pool.length));
    setSession(shuffled);
    setCurrent(shuffled[0] || null);
    setMode("mock");
    setNotes("");
    setSavedNotes("");
    recordActivity();
  }

  function saveNote() {
    if (!current) return;
    const key = `ipbd.notes.${current.slug}`;
    window.localStorage.setItem(key, notes);
    setSavedNotes("Notes saved on this device.");
    recordActivity();
  }

  function rate(value: number) {
    if (!current) return;
    setRating(value);
    reviewQuestion(current.slug, value);
    setSavedNotes("Self-rating saved. Spaced repetition date updated.");
  }

  return <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_320px]">
    <section className="space-y-5">
      <div className="panel p-5 sm:p-6"><div className="flex flex-wrap items-center justify-between gap-3"><div><p className="text-[10px] font-bold uppercase tracking-[0.18em] text-mint">Practice workspace</p><h2 className="mt-2 text-xl font-semibold text-white">Pick a question and think out loud</h2><p className="mt-2 text-sm leading-6 text-slate-400">প্রথমে problem restate করো, assumptions জিজ্ঞেস করো, তারপর approach ও complexity বোঝাও।</p></div><span className="rounded-full border border-mint/20 bg-mint/10 px-3 py-1.5 text-xs text-mint">Local-only notes</span></div>
        <div className="mt-5 grid gap-3 sm:grid-cols-2"><label className="text-xs text-slate-500">Topic<select value={category} onChange={(event) => setCategory(event.target.value)} className="mt-2 w-full rounded-xl border border-white/10 bg-[#0b101c] px-3 py-3 text-sm text-slate-200"><option value="all">All topics</option><option value="dsa">DSA</option><option value="system-design">System Design</option><option value="database">Database</option><option value="behavioral">Behavioral</option><option value="languages">Languages</option><option value="bangladesh">Bangladesh interviews</option></select></label><label className="text-xs text-slate-500">Difficulty<select value={difficulty} onChange={(event) => setDifficulty(event.target.value)} className="mt-2 w-full rounded-xl border border-white/10 bg-[#0b101c] px-3 py-3 text-sm text-slate-200"><option value="all">All levels</option><option>Easy</option><option>Medium</option><option>Hard</option></select></label></div>
        <div className="mt-4 flex flex-wrap gap-2"><button onClick={chooseQuestion} disabled={!pool.length} className="rounded-xl bg-mint px-4 py-3 text-sm font-bold text-ink transition hover:bg-white disabled:opacity-40">Pick random question ↗</button><button onClick={startMock} disabled={!pool.length} className="rounded-xl border border-white/10 px-4 py-3 text-sm font-semibold text-slate-300 transition hover:border-mint/30 hover:text-mint disabled:opacity-40">Start 5-question mock</button></div>
      </div>
      {current ? <div className="panel p-5 sm:p-6"><div className="flex flex-wrap items-center justify-between gap-3"><span className="text-xs uppercase tracking-[0.14em] text-slate-500">{mode === "mock" ? `Mock interview · ${session.findIndex((item) => item.slug === current.slug) + 1}/${session.length}` : "Selected question"}</span><span className="text-xs text-slate-500">{current.minutes} minute target</span></div><h3 className="mt-3 text-2xl font-bold tracking-tight text-white">{current.title}</h3><p className="mt-3 leading-7 text-slate-300">{current.problem}</p><div className="mt-4 flex flex-wrap gap-2">{current.tags.map((tag) => <span key={tag} className="rounded-lg border border-white/10 px-2.5 py-1.5 text-[11px] text-slate-500">{tag}</span>)}</div><div className="mt-6"><label className="text-xs font-semibold text-slate-300">Your approach / interview notes<textarea value={notes} onChange={(event) => setNotes(event.target.value)} rows={6} placeholder="Write assumptions, brute force, optimized approach, complexity and edge cases…" className="mt-2 w-full resize-y rounded-xl border border-white/10 bg-[#080d17] p-3 text-sm leading-6 text-slate-200 outline-none placeholder:text-slate-600 focus:border-mint/30" /></label><div className="mt-3 flex flex-wrap items-center justify-between gap-3"><button onClick={saveNote} className="rounded-lg border border-white/10 px-3 py-2 text-xs font-semibold text-slate-300 hover:border-mint/30 hover:text-mint">Save notes on device</button>{savedNotes && <span role="status" className="text-xs text-mint">{savedNotes}</span>}</div></div><div className="mt-6 border-t border-white/[0.07] pt-5"><p className="text-xs font-semibold text-slate-300">Self-rate this attempt</p><div className="mt-3 flex flex-wrap gap-2">{[{ value: 1, label: "Again" }, { value: 3, label: "Good" }, { value: 5, label: "Easy" }].map((option) => <button key={option.value} onClick={() => rate(option.value)} className={`rounded-lg border px-4 py-2.5 text-xs font-semibold ${rating === option.value ? "border-mint/40 bg-mint/10 text-mint" : "border-white/10 text-slate-400 hover:text-white"}`}>{option.label}</button>)}</div></div><div className="mt-6"><a href={`/interview-prep/questions/${current.slug}/`} className="text-sm font-semibold text-sky hover:text-mint">Open full solution and explanation ↗</a></div>{mode === "mock" && <div className="mt-5 flex justify-between gap-3 border-t border-white/[0.07] pt-4"><button onClick={() => { const index = session.findIndex((item) => item.slug === current.slug); const next = session[Math.max(0, index - 1)]; if (next) setCurrent(next); }} className="rounded-lg border border-white/10 px-3 py-2 text-xs text-slate-400">Previous</button><button onClick={() => { const index = session.findIndex((item) => item.slug === current.slug); const next = session[index + 1]; if (next) { setCurrent(next); setNotes(""); setSavedNotes(""); } }} className="rounded-lg bg-mint px-3 py-2 text-xs font-bold text-ink">Next question →</button></div>}</div> : <div className="panel flex min-h-60 flex-col items-center justify-center p-8 text-center"><span className="text-3xl text-mint">◉</span><h3 className="mt-4 text-lg font-semibold text-slate-100">Your practice session starts here</h3><p className="mt-2 max-w-sm text-sm leading-6 text-slate-500">একটি random prompt নাও, আগে নিজে solve করো, তারপর full explanation খুলে নিজের উত্তর যাচাই করো।</p></div>}
      {session.length > 0 && <div><h3 className="mb-3 text-sm font-semibold text-slate-300">Recent session picks</h3><div className="grid gap-3 sm:grid-cols-2">{session.map((item) => <QuestionCard key={item.slug} question={item} />)}</div></div>}
    </section>
    <aside className="space-y-4"><Timer initialMinutes={30} /><div className="panel p-5"><p className="text-xs font-bold uppercase tracking-[0.15em] text-slate-500">Interview loop</p><div className="mt-4 space-y-4">{[{n:"01",t:"Clarify",d:"Input, constraints, examples"},{n:"02",t:"Plan",d:"Brute force → optimized approach"},{n:"03",t:"Implement",d:"Readable code and invariants"},{n:"04",t:"Verify",d:"Run examples and edge cases"},{n:"05",t:"Reflect",d:"Complexity and trade-offs"}].map((step) => <div key={step.n} className="flex gap-3"><span className="font-mono text-xs text-mint">{step.n}</span><div><p className="text-sm font-semibold text-slate-200">{step.t}</p><p className="mt-1 text-xs leading-5 text-slate-500">{step.d}</p></div></div>)}</div></div><div className="rounded-2xl border border-sky/15 bg-sky/[0.04] p-5"><p className="text-sm font-semibold text-sky">বাংলা + English practice</p><p className="mt-2 text-xs leading-6 text-slate-400">নিজের reasoning বাংলায় পরিষ্কার করো; interview-এর প্রয়োজন অনুযায়ী core technical terms ইংরেজিতে concise করে বলার অভ্যাস করো।</p></div></aside>
  </div>;
}
