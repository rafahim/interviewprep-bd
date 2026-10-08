"use client";

import { useEffect, useState } from "react";
import type { ProgressStatus } from "@/types";
import { readBookmarks, readProgress, saveStatus, toggleBookmark } from "@/lib/progress";

export function QuestionActions({ slug, title, content }: { slug: string; title: string; content: string }) {
  const [bookmarked, setBookmarked] = useState(false);
  const [status, setStatus] = useState<ProgressStatus>("todo");
  const [message, setMessage] = useState("");
  useEffect(() => {
    setBookmarked(readBookmarks().includes(slug));
    setStatus(readProgress()[slug]?.status || "todo");
  }, [slug]);
  async function share() {
    const url = window.location.href;
    try {
      if (navigator.share) await navigator.share({ title, url });
      else { await navigator.clipboard.writeText(url); setMessage("Link copied to clipboard."); }
    } catch { setMessage("Share was cancelled or unavailable."); }
  }
  async function copy() {
    try { await navigator.clipboard.writeText(`${title}\n\n${content}`); setMessage("Question and explanation copied."); }
    catch { setMessage("Clipboard access is unavailable in this browser."); }
  }
  async function feedback(rating: "helpful" | "needs-work") {
    try {
      const response = await fetch("/interview-prep/api/feedback/", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ slug, rating }) });
      const data = await response.json();
      setMessage(data.persisted ? "Thanks — feedback saved." : "Thanks — feedback received for this session; configure Supabase to store it.");
    } catch { setMessage("Feedback could not be sent. Please try again."); }
  }
  function updateStatus(next: ProgressStatus) { saveStatus(slug, next); setStatus(next); setMessage(`Status updated: ${next.replace("-", " ")}.`); }
  return <div className="panel space-y-4 p-4">
    <div><p className="text-[10px] font-bold uppercase tracking-[0.16em] text-slate-500">Your workspace</p><select aria-label="Question progress status" value={status} onChange={(event) => updateStatus(event.target.value as ProgressStatus)} className="mt-2 w-full rounded-xl border border-white/10 bg-[#0b101c] px-3 py-2.5 text-xs text-slate-200"><option value="todo">To do</option><option value="in-progress">In progress</option><option value="solved">Solved</option><option value="needs-review">Needs review</option></select></div>
    <div className="grid grid-cols-2 gap-2"><button onClick={() => { setBookmarked(toggleBookmark(slug)); setMessage(bookmarked ? "Removed from bookmarks." : "Saved to bookmarks."); }} className="rounded-xl border border-white/10 px-3 py-2.5 text-xs font-semibold text-slate-300 transition hover:border-mint/40 hover:text-mint">{bookmarked ? "★ Bookmarked" : "☆ Bookmark"}</button><button onClick={share} className="rounded-xl border border-white/10 px-3 py-2.5 text-xs font-semibold text-slate-300 transition hover:border-mint/40 hover:text-mint">Share ↗</button></div>
    <button onClick={copy} className="w-full rounded-xl border border-white/10 px-3 py-2.5 text-xs font-semibold text-slate-300 transition hover:border-mint/40 hover:text-mint">Copy question + explanation</button>
    <div className="border-t border-white/[0.07] pt-3"><p className="text-xs font-semibold text-slate-300">Was this explanation helpful?</p><div className="mt-2 grid grid-cols-2 gap-2"><button onClick={() => feedback("helpful")} className="rounded-lg bg-white/[0.04] px-2 py-2 text-xs text-slate-400 hover:text-mint">Yes, helpful</button><button onClick={() => feedback("needs-work")} className="rounded-lg bg-white/[0.04] px-2 py-2 text-xs text-slate-400 hover:text-amber">Needs work</button></div></div>
    {message && <p role="status" className="text-xs leading-5 text-mint">{message}</p>}
  </div>;
}
