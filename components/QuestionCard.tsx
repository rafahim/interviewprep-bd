import Link from "next/link";
import type { QuestionIndexItem } from "@/types";
import { CATEGORY_LABELS } from "@/lib/categories";
import { difficultyTone } from "@/lib/utils";

export function QuestionCard({ question, index }: { question: QuestionIndexItem; index?: number }) {
  return <article className="group panel flex h-full flex-col p-5 transition duration-200 hover:-translate-y-0.5 hover:border-mint/30 hover:shadow-glow">
    <div className="flex items-center justify-between gap-3"><span className="text-[11px] font-semibold uppercase tracking-[0.14em] text-slate-500">{CATEGORY_LABELS[question.category]}</span><span className={`rounded-full border px-2.5 py-1 text-[10px] font-semibold ${difficultyTone(question.difficulty)}`}>{question.difficulty}</span></div>
    <Link href={`/questions/${question.slug}/`} className="mt-4 block"><h3 className="text-base font-semibold leading-snug text-slate-100 transition group-hover:text-mint">{index ? <span className="mr-2 font-mono text-xs text-slate-600">{String(index).padStart(2, "0")}</span> : null}{question.title}</h3></Link>
    <p className="mt-2 line-clamp-3 flex-1 text-sm leading-6 text-slate-400">{question.problem}</p>
    <div className="mt-4 flex flex-wrap gap-1.5">{question.tags.slice(0, 3).map((tag) => <span key={tag} className="rounded-md border border-white/[0.07] bg-white/[0.025] px-2 py-1 text-[10px] text-slate-500">{tag}</span>)}</div>
    <div className="mt-5 flex items-center justify-between border-t border-white/[0.07] pt-4 text-xs text-slate-500"><span>{question.minutes} min · {question.frequency} frequency</span><Link href={`/questions/${question.slug}/`} className="font-semibold text-slate-300 transition group-hover:text-mint">Study ↗</Link></div>
  </article>;
}
