import type { QuestionCategory } from "@/types";

export const CATEGORY_LABELS: Record<QuestionCategory, string> = {
  dsa: "DSA & Algorithms",
  "system-design": "System Design",
  database: "Database",
  behavioral: "Behavioral",
  languages: "Languages & Runtime",
  bangladesh: "Bangladesh Interviews"
};

export const CATEGORY_DESCRIPTIONS: Record<QuestionCategory, string> = {
  dsa: "Arrays, graphs, linked lists, dynamic programming and core patterns.",
  "system-design": "Design reliable systems, APIs, storage, queues and distributed services.",
  database: "SQL, indexes, transactions, normalization and database internals.",
  behavioral: "STAR-based examples for teamwork, ownership, feedback and growth.",
  languages: "Runtime behavior, async code, types, memory and language fundamentals.",
  bangladesh: "Practical interview preparation for Bangladesh and remote tech roles."
};

export const CATEGORY_ORDER: QuestionCategory[] = ["dsa", "system-design", "database", "behavioral", "languages", "bangladesh"];
