export function cx(...values: Array<string | false | null | undefined>): string {
  return values.filter(Boolean).join(" ");
}

export function difficultyTone(value: string): string {
  if (value === "Easy") return "border-emerald-400/20 bg-emerald-400/10 text-emerald-200";
  if (value === "Hard") return "border-rose-400/20 bg-rose-400/10 text-rose-200";
  return "border-amber-300/20 bg-amber-300/10 text-amber-100";
}

export function formatDate(value: string | null): string {
  if (!value) return "Not scheduled";
  return new Intl.DateTimeFormat("en-BD", { day: "numeric", month: "short", year: "numeric" }).format(new Date(value));
}
