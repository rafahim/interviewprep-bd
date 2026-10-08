import type { Metadata } from "next";
import { Flashcards } from "@/components/Flashcards";
import { getQuestionIndex } from "@/lib/questions";
import { pageMetadata } from "@/lib/seo";

export const metadata: Metadata = pageMetadata("Flashcards", "Auto-generated interview recall flashcards with SM-2 spaced repetition and local review scheduling.", "/flashcards/");

export default function FlashcardsPage() {
  return <div className="mx-auto max-w-7xl px-5 py-10 sm:px-8 sm:py-14"><Flashcards questions={getQuestionIndex()} /></div>;
}
