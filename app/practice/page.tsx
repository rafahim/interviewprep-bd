import type { Metadata } from "next";
import { PracticeRoom } from "@/components/PracticeRoom";
import { getQuestionIndex } from "@/lib/questions";
import { pageMetadata } from "@/lib/seo";

export const metadata: Metadata = pageMetadata("Practice Mode", "Timed mock interviews, random question picker, device-local notes and self-rating for interview preparation.", "/practice/");

export default function PracticePage() {
  return <div className="mx-auto max-w-7xl px-5 py-10 sm:px-8 sm:py-14"><div className="mb-8 max-w-3xl"><p className="text-xs font-bold uppercase tracking-[0.18em] text-mint">Practice / অনুশীলন</p><h1 className="mt-3 text-3xl font-bold tracking-tight text-white sm:text-5xl">Train under interview conditions.</h1><p className="mt-4 text-sm leading-7 text-slate-400 sm:text-base">Random prompt, 5-question mock, timer, private notes এবং self-rating—সব progress browser-এ save হয়।</p></div><PracticeRoom questions={getQuestionIndex()} /></div>;
}
