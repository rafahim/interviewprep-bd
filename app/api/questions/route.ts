import { NextResponse } from "next/server";
import { getQuestionIndex } from "@/lib/questions";

export const dynamic = "force-static";

export async function GET() {
  return NextResponse.json(getQuestionIndex(), { headers: { "Cache-Control": "public, max-age=3600, s-maxage=86400" } });
}
