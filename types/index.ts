export type Difficulty = "Easy" | "Medium" | "Hard";
export type ProgressStatus = "todo" | "in-progress" | "solved" | "needs-review";
export type QuestionCategory = "dsa" | "system-design" | "database" | "behavioral" | "languages" | "bangladesh";

export type FlashcardData = {
  front: string;
  back: string;
};

export type QuestionMeta = {
  slug: string;
  title: string;
  category: QuestionCategory;
  topic: string;
  difficulty: Difficulty;
  companies: string[];
  languages: string[];
  frequency: "High" | "Medium" | "Low";
  minutes: number;
  problem: string;
  approach: string;
  complexity: { time: string; space: string };
  edges: string[];
  related: string[];
  front: string;
  back: string;
  summary: string;
  tags: string[];
  examples: { input: string; output: string };
  order: number;
};

export type Question = QuestionMeta & { content: string };
export type QuestionIndexItem = Omit<Question, "content">;

export type ProgressRecord = {
  status: ProgressStatus;
  updatedAt: string;
  repetitions: number;
  interval: number;
  easeFactor: number;
  nextReview: string | null;
  lastRating?: number;
};

export type ProgressMap = Record<string, ProgressRecord>;
