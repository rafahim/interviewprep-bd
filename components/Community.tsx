"use client";

const repo = process.env.NEXT_PUBLIC_GISCUS_REPO || "rafahim/interviewprep-bd";
const repoId = process.env.NEXT_PUBLIC_GISCUS_REPO_ID || "";
const category = process.env.NEXT_PUBLIC_GISCUS_CATEGORY || "General";
const categoryId = process.env.NEXT_PUBLIC_GISCUS_CATEGORY_ID || "";

export function Community({ slug }: { slug?: string }) {
  const discussion = `https://github.com/${repo}/discussions`;
  const configured = Boolean(repoId && categoryId);
  const giscus = `https://giscus.app/iframe.html?origin=https%3A%2F%2Frafahim.com&session=&repo=${encodeURIComponent(repo)}&repoId=${encodeURIComponent(repoId)}&category=${encodeURIComponent(category)}&categoryId=${encodeURIComponent(categoryId)}&mapping=${encodeURIComponent(slug ? "specific" : "pathname")}&term=${encodeURIComponent(slug || "")}&strict=0&reactionsEnabled=1&emitMetadata=0&inputPosition=top&theme=dark&lang=bn`;
  return <section className="panel p-5 sm:p-6"><div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between"><div><p className="text-[10px] font-bold uppercase tracking-[0.16em] text-mint">Community</p><h3 className="mt-2 text-lg font-semibold text-white">Improve the question bank</h3><p className="mt-2 max-w-xl text-sm leading-6 text-slate-400">Correction, better explanation, translation or a new question যোগ করতে GitHub Pull Request খুলো। Discussion-এর জন্য Giscus configure করা যায়।</p></div><a href={`https://github.com/${repo}/pulls`} target="_blank" rel="noreferrer" className="shrink-0 rounded-xl border border-white/10 px-4 py-2.5 text-xs font-bold text-slate-200 transition hover:border-mint/30 hover:text-mint">Open a GitHub PR ↗</a></div>{configured ? <div className="mt-6 overflow-hidden rounded-xl border border-white/10 bg-[#080d17]"><iframe title="Giscus community discussion" src={giscus} loading="lazy" className="h-[420px] w-full border-0" /></div> : <div className="mt-5 rounded-xl border border-dashed border-white/10 bg-white/[0.02] p-4"><p className="text-sm font-semibold text-slate-300">Comments are optional</p><p className="mt-1 text-xs leading-5 text-slate-500">Set `NEXT_PUBLIC_GISCUS_REPO_ID` and `NEXT_PUBLIC_GISCUS_CATEGORY_ID` in your deployment environment to enable Giscus. Until then, the repo Discussions link remains available.</p><a href={discussion} target="_blank" rel="noreferrer" className="mt-3 inline-block text-xs font-semibold text-sky hover:text-mint">Open GitHub Discussions ↗</a></div>}</section>;
}
