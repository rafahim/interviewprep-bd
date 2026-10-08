import { NextResponse } from "next/server";
import { getAllQuestions } from "@/lib/questions";
import { getSupabaseAdmin } from "@/lib/supabase";

export async function POST(request: Request) {
  let payload: { slug?: string; rating?: string };
  try {
    payload = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON body." }, { status: 400 });
  }
  if (!payload.slug || !["helpful", "needs-work"].includes(payload.rating || "")) {
    return NextResponse.json({ error: "A valid slug and rating are required." }, { status: 400 });
  }
  if (!getAllQuestions().some((question) => question.slug === payload.slug)) {
    return NextResponse.json({ error: "Question not found." }, { status: 404 });
  }
  const supabase = getSupabaseAdmin();
  if (!supabase) return NextResponse.json({ ok: true, persisted: false });
  const { error } = await supabase.from("question_feedback").insert({ slug: payload.slug, rating: payload.rating });
  if (error) return NextResponse.json({ error: "Feedback storage is not configured correctly." }, { status: 503 });
  return NextResponse.json({ ok: true, persisted: true });
}
