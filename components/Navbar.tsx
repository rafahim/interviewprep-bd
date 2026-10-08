import Link from "next/link";
import { Search } from "@/components/Search";
import { LanguageToggle } from "@/components/LanguageToggle";

const links = [
  { href: "/questions/", label: "Questions" },
  { href: "/practice/", label: "Practice" },
  { href: "/flashcards/", label: "Flashcards" },
  { href: "/progress/", label: "Progress" }
];

export function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-white/[0.07] bg-ink/85 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-5 py-3.5 sm:px-8">
        <Link href="/" className="group flex min-w-0 items-center gap-2.5">
          <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-mint text-sm font-black text-ink shadow-glow">IP</span>
          <span className="min-w-0"><span className="block truncate text-sm font-bold tracking-tight text-white sm:text-base">InterviewPrep <span className="text-mint">BD</span></span><span className="hidden text-[10px] tracking-[0.16em] text-slate-500 sm:block">BY RA FAHIM</span></span>
        </Link>
        <nav className="hidden items-center gap-5 lg:flex">
          {links.map((link) => <Link key={link.href} href={link.href} className="text-sm text-slate-400 transition hover:text-white">{link.label}</Link>)}
        </nav>
        <div className="flex shrink-0 items-center gap-2.5"><Search /><LanguageToggle /></div>
      </div>
      <nav className="mx-auto flex max-w-7xl gap-5 overflow-x-auto px-5 pb-3 text-xs text-slate-400 sm:px-8 lg:hidden">
        {links.map((link) => <Link key={link.href} href={link.href} className="whitespace-nowrap transition hover:text-mint">{link.label}</Link>)}
      </nav>
    </header>
  );
}
