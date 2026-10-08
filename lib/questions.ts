import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import type { Question, QuestionIndexItem, QuestionMeta } from "@/types";

const CONTENT_DIR = path.join(process.cwd(), "content");
const CATEGORY_DIRS = ["dsa", "system-design", "database", "behavioral", "languages", "bangladesh"];

function getMdxFiles(dir: string): string[] {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const entryPath = path.join(dir, entry.name);
    if (entry.isDirectory()) return getMdxFiles(entryPath);
    return entry.isFile() && entry.name.endsWith(".mdx") ? [entryPath] : [];
  });
}

function readQuestion(filePath: string): Question {
  const source = fs.readFileSync(filePath, "utf8");
  const parsed = matter(source);
  const meta = parsed.data as QuestionMeta;
  if (!meta.slug || !meta.title || !meta.category) {
    throw new Error(`Missing required question frontmatter in ${filePath}`);
  }
  return { ...meta, content: parsed.content.trim() };
}

export function getAllQuestions(): Question[] {
  return CATEGORY_DIRS.flatMap((category) => getMdxFiles(path.join(CONTENT_DIR, category)))
    .map(readQuestion)
    .sort((a, b) => a.order - b.order || a.title.localeCompare(b.title));
}

export function getQuestionIndex(): QuestionIndexItem[] {
  return getAllQuestions().map(({ content, ...question }) => question);
}

export function getQuestionBySlug(slug: string): Question | undefined {
  const file = getAllQuestions().find((question) => question.slug === slug);
  return file;
}
