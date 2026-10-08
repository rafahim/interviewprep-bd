import type { Metadata } from "next";
import { ProgressDashboard } from "@/components/ProgressDashboard";
import { getQuestionIndex } from "@/lib/questions";
import { pageMetadata } from "@/lib/seo";

export const metadata: Metadata = pageMetadata("Progress Dashboard", "Track solved questions, review dates, study streaks and local-first interview preparation progress.", "/progress/");

export default function ProgressPage() {
  return <div className="mx-auto max-w-7xl px-5 py-10 sm:px-8 sm:py-14"><div className="mb-8 max-w-3xl"><p className="text-xs font-bold uppercase tracking-[0.18em] text-mint">Progress / অগ্রগতি</p><h1 className="mt-3 text-3xl font-bold tracking-tight text-white sm:text-5xl">Small steps, visible progress.</h1><p className="mt-4 text-sm leading-7 text-slate-400 sm:text-base">Solved, in-progress, todo, needs-review, streak এবং due date—আপনার progress server-এ পাঠানো হয় না; এই browser-এই থাকে।</p></div><ProgressDashboard questions={getQuestionIndex()} /></div>;
}
