import type { Metadata } from "next";
import { QuestionBrowser } from "@/components/QuestionBrowser";
import { Community } from "@/components/Community";
import { getQuestionIndex } from "@/lib/questions";
import { pageMetadata, SITE_URL } from "@/lib/seo";

export const metadata: Metadata = pageMetadata("Question Bank", "Browse 60 interview questions with Bengali explanations, difficulty, company, language and topic filters.", "/questions/");

export default function QuestionsPage({ searchParams }: { searchParams: { category?: string } }) {
  const questions = getQuestionIndex();
  const initialCategory = CATEGORY_ORDER.find((category) => category === searchParams?.category) || "";
  const schema = { "@context": "https://schema.org", "@type": "ItemList", name: "InterviewPrep BD Question Bank", numberOfItems: questions.length, itemListElement: questions.map((question, index) => ({ "@type": "ListItem", position: index + 1, name: question.title, url: `${SITE_URL}/questions/${question.slug}/` })) };
  return <div className="mx-auto max-w-7xl px-5 py-10 sm:px-8 sm:py-14"><script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} /><div className="max-w-3xl"><p className="text-xs font-bold uppercase tracking-[0.18em] text-mint">Question bank / প্রশ্নভান্ডার</p><h1 className="mt-3 text-3xl font-bold tracking-tight text-white sm:text-5xl">Find the right question.</h1><p className="mt-4 text-sm leading-7 text-slate-400 sm:text-base">Difficulty, topic, company, language এবং frequency দিয়ে filter করো। প্রতিটি lesson-এ Bengali explanation, interview reasoning এবং relevant edge cases রয়েছে।</p></div><div className="mt-8"><QuestionBrowser questions={questions} initialCategory={initialCategory} /></div><div className="mt-12"><Community /></div></div>;
}
