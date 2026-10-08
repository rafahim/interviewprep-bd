import type { ProgressMap, ProgressRecord, ProgressStatus } from "@/types";
import { calculateSM2 } from "@/lib/sm2";

const PROGRESS_KEY = "ipbd.progress.v1";
const ACTIVITY_KEY = "ipbd.activity.v1";

export function readProgress(): ProgressMap {
  if (typeof window === "undefined") return {};
  try {
    return JSON.parse(window.localStorage.getItem(PROGRESS_KEY) || "{}") as ProgressMap;
  } catch {
    return {};
  }
}

export function readActivity(): string[] {
  if (typeof window === "undefined") return [];
  try {
    const value = JSON.parse(window.localStorage.getItem(ACTIVITY_KEY) || "[]");
    return Array.isArray(value) ? value.filter((item) => typeof item === "string") : [];
  } catch {
    return [];
  }
}

export function recordActivity(now = new Date()): void {
  if (typeof window === "undefined") return;
  const day = now.toISOString().slice(0, 10);
  const activity = new Set(readActivity());
  activity.add(day);
  window.localStorage.setItem(ACTIVITY_KEY, JSON.stringify([...activity].sort().slice(-365)));
}

export function saveStatus(slug: string, status: ProgressStatus): ProgressMap {
  const progress = readProgress();
  const current = progress[slug] || { status: "todo", updatedAt: new Date().toISOString(), repetitions: 0, interval: 0, easeFactor: 2.5, nextReview: null };
  progress[slug] = { ...current, status, updatedAt: new Date().toISOString() };
  if (status === "solved") {
    const next = calculateSM2(current, 4);
    progress[slug] = { ...progress[slug], ...next, lastRating: 4 };
  }
  if (typeof window !== "undefined") window.localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
  recordActivity();
  return progress;
}

export function reviewQuestion(slug: string, rating: number): ProgressMap {
  const progress = readProgress();
  const current: ProgressRecord = progress[slug] || { status: "needs-review", updatedAt: new Date().toISOString(), repetitions: 0, interval: 0, easeFactor: 2.5, nextReview: null };
  const next = calculateSM2(current, rating);
  progress[slug] = { ...current, ...next, status: rating < 3 ? "needs-review" : "solved", lastRating: rating, updatedAt: new Date().toISOString() };
  if (typeof window !== "undefined") window.localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
  recordActivity();
  return progress;
}

export function getCurrentStreak(activity = readActivity(), now = new Date()): number {
  const days = new Set(activity);
  let cursor = new Date(now);
  let key = cursor.toISOString().slice(0, 10);
  if (!days.has(key)) {
    cursor.setDate(cursor.getDate() - 1);
    key = cursor.toISOString().slice(0, 10);
    if (!days.has(key)) return 0;
  }
  let streak = 0;
  while (days.has(key)) {
    streak += 1;
    cursor.setDate(cursor.getDate() - 1);
    key = cursor.toISOString().slice(0, 10);
  }
  return streak;
}

export function toggleBookmark(slug: string): boolean {
  if (typeof window === "undefined") return false;
  const key = "ipbd.bookmarks.v1";
  let values: string[] = [];
  try {
    values = JSON.parse(window.localStorage.getItem(key) || "[]") as string[];
  } catch {
    values = [];
  }
  const next = new Set(values);
  if (next.has(slug)) next.delete(slug);
  else next.add(slug);
  window.localStorage.setItem(key, JSON.stringify([...next]));
  recordActivity();
  return next.has(slug);
}

export function readBookmarks(): string[] {
  if (typeof window === "undefined") return [];
  try {
    const values = JSON.parse(window.localStorage.getItem("ipbd.bookmarks.v1") || "[]");
    return Array.isArray(values) ? values.filter((item) => typeof item === "string") : [];
  } catch {
    return [];
  }
}
