import { codeToHtml } from "shiki";

export async function CodeBlock({ code, language = "text", title }: { code: string; language?: string; title?: string }) {
  const html = await codeToHtml(code, { lang: language, theme: "github-dark" });
  return <div className="my-4 overflow-hidden rounded-2xl border border-line bg-[#080d17]">{title && <div className="border-b border-line px-4 py-2 text-xs text-slate-500">{title}</div>}<div className="pretty-code" dangerouslySetInnerHTML={{ __html: html }} /></div>;
}
