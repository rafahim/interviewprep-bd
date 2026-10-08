import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t border-white/5 mt-20">
      <div className="mx-auto flex max-w-7xl flex-col gap-3 px-5 py-7 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between sm:px-8">
        <p>Built with ❤️ by <a className="text-slate-300 hover:text-mint" href="https://rafahim.com">RA Fahim</a> · <a className="text-slate-300 hover:text-mint" href="https://rafahim.com">rafahim.com</a> · © 2026 RA Fahim</p>
        <div className="flex flex-wrap gap-4">
          <Link className="hover:text-slate-200" href="/questions/">Questions</Link>
          <Link className="hover:text-slate-200" href="/practice/">Practice</Link>
          <a className="hover:text-slate-200" href="https://github.com/rafahim/interviewprep-bd">Contribute on GitHub</a>
        </div>
      </div>
    </footer>
  );
}
