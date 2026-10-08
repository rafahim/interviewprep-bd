import Link from "next/link";

export default function NotFound() {
  return <div className="mx-auto flex min-h-[55vh] max-w-3xl flex-col items-center justify-center px-5 text-center"><p className="font-mono text-sm text-mint">404 · NOT FOUND</p><h1 className="mt-4 text-3xl font-bold text-white">Question not found</h1><p className="mt-3 text-sm leading-6 text-slate-500">এই URL-এ কোনো lesson পাওয়া যায়নি। Question bank থেকে অন্য একটি বেছে নাও।</p><Link href="/questions/" className="mt-6 rounded-xl bg-mint px-5 py-3 text-sm font-bold text-ink">Browse questions</Link></div>;
}
