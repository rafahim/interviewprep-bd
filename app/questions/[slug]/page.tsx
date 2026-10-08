import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { compileMDX } from "next-mdx-remote/rsc";
import rehypePrettyCode from "rehype-pretty-code";
import { QuestionActions } from "@/components/QuestionActions";
import { QuestionCard } from "@/components/QuestionCard";
import { Community } from "@/components/Community";
import { CATEGORY_LABELS } from "@/lib/categories";
import { getAllQuestions, getQuestionBySlug, getQuestionIndex } from "@/lib/questions";
import { difficultyTone } from "@/lib/utils";
import { pageMetadata, SITE_URL } from "@/lib/seo";

export function generateStaticParams() {
  return getAllQuestions().map((question) => ({ slug: question.slug }));
}

export async function generateMetadata({ params }: { params: { slug: string } }): Promise<Metadata> {
  const question = getQuestionBySlug(params.slug);
  if (!question) return pageMetadata("Question Not Found", "The requested interview question could not be found.", "/questions/");
  return pageMetadata(question.title, question.problem, `/questions/${question.slug}/`);
}

export default async function QuestionDetailPage({ params }: { params: { slug: string } }) {
  const question = getQuestionBySlug(params.slug);
  if (!question) notFound();
  const { content } = await compileMDX({
    source: question.content,
    options: { mdxOptions: { rehypePlugins: [[rehypePrettyCode, { theme: "github-dark", keepBackground: false }]] } }
  });
  const all = getQuestionIndex();
  const related = question.related.map((slug) => all.find((item) => item.slug === slug)).filter((item) => item !== undefined).slice(0, 3);
  const schema = {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    headline: question.title,
    description: question.problem,
    inLanguage: ["bn", "en"],
    url: `${SITE_URL}/questions/${question.slug}/`,
    author: { "@type": "Person", name: "RA Fahim", url: "https://rafahim.com" },
    publisher: { "@type": "Organization", name: "InterviewPrep BD", url: `${SITE_URL}/` },
    keywords: question.tags.join(", ")
  };
  return <div className="mx-auto max-w-7xl px-5 py-8 sm:px-8 sm:py-12"><script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} /><div className="mb-7 flex flex-wrap items-center gap-2 text-xs text-slate-600"><Link href="/questions/" className="hover:text-mint">Question bank</Link><span>/</span><span>{CATEGORY_LABELS[question.category]}</span><span>/</span><span className="text-slate-400">{question.title}</span></div><div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_300px]"><main className="min-w-0"><div className="flex flex-wrap items-center gap-2"><span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5 text-[11px] font-semibold text-slate-300">{CATEGORY_LABELS[question.category]}</span><span className={`rounded-full border px-3 py-1.5 text-[11px] font-semibold ${difficultyTone(question.difficulty)}`}>{question.difficulty}</span><span className="rounded-full border border-white/10 px-3 py-1.5 text-[11px] text-slate-500">{question.minutes} min</span><span className="rounded-full border border-white/10 px-3 py-1.5 text-[11px] text-slate-500">{question.frequency} frequency</span></div><h1 className="mt-5 text-3xl font-bold leading-tight tracking-tight text-white sm:text-5xl">{question.title}</h1><p className="mt-4 max-w-3xl text-base leading-8 text-slate-400">{question.problem}</p><div className="mt-5 flex flex-wrap gap-2">{question.companies.map((company) => <span key={company} className="rounded-lg border border-white/[0.07] bg-white/[0.025] px-2.5 py-1.5 text-[11px] text-slate-500">{company}</span>)}{question.languages.map((language) => <span key={language} className="rounded-lg border border-sky/15 bg-sky/[0.04] px-2.5 py-1.5 text-[11px] text-sky">{language}</span>)}</div><div className="mt-8 rounded-2xl border border-white/[0.07] bg-[#0a0f1a]/80 p-5 sm:p-7"><article className="prose prose-invert max-w-none">{content}</article></div><div className="mt-8"><Community slug={question.slug} /></div>{related.length > 0 && <section className="mt-10"><div className="flex items-end justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-[0.16em] text-mint">Keep learning</p><h2 className="mt-2 text-xl font-bold text-white">Related questions</h2></div><Link href="/questions/" className="text-xs font-semibold text-sky hover:text-mint">All questions ↗</Link></div><div className="mt-4 grid gap-3 md:grid-cols-3">{related.map((item) => <QuestionCard key={item.slug} question={item} />)}</div></section>}<div className="mt-10 flex items-center justify-between border-t border-white/[0.07] pt-5"><Link href="/questions/" className="text-sm font-semibold text-slate-400 hover:text-mint">← Back to question bank</Link><a href="https://github.com/rafahim" target="_blank" rel="noreferrer" className="text-xs text-slate-600 hover:text-slate-300">Improve this lesson ↗</a></div></main><aside className="space-y-4 lg:sticky lg:top-28 lg:self-start"><QuestionActions slug={question.slug} title={question.title} content={`${question.problem}\n\n${question.approach}`} /><div className="panel p-4"><p className="text-[10px] font-bold uppercase tracking-[0.15em] text-slate-500">Quick facts</p><div className="mt-3 space-y-3 text-xs">{question.category === "dsa" ? <><div className="flex justify-between gap-3"><span className="text-slate-500">Time complexity</span><span className="text-right font-mono text-slate-200">{question.complexity.time}</span></div><div className="flex justify-between gap-3"><span className="text-slate-500">Extra space</span><span className="text-right font-mono text-slate-200">{question.complexity.space}</span></div></> : <><div className="flex justify-between gap-3"><span className="text-slate-500">Topic</span><span className="text-right text-slate-200">{question.topic}</span></div><div className="flex justify-between gap-3"><span className="text-slate-500">Focus</span><span className="text-right text-slate-200">{question.complexity.space}</span></div></>}<div className="flex justify-between gap-3"><span className="text-slate-500">Study target</span><span className="text-slate-200">{question.minutes} min</span></div></div></div><div className="rounded-2xl border border-sky/15 bg-sky/[0.04] p-4"><p className="text-sm font-semibold text-sky">Interview tip</p><p className="mt-2 text-xs leading-6 text-slate-400">প্রথমে explanation না দেখে solve করার চেষ্টা করো। তারপর invariant, edge cases এবং complexity নিজের ভাষায় explain করো।</p></div></aside></div></div>;
}
