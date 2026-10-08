import type { Metadata } from "next";

export const SITE_NAME = "InterviewPrep BD";
export const SITE_URL = "https://rafahim.com/interview-prep";
export const OWNER_URL = "https://rafahim.com";
export const DEFAULT_DESCRIPTION = "Free coding interview questions with Bengali explanations, Python and JavaScript solutions, system design, behavioral STAR answers and local interview guidance.";
export const KEYWORDS = ["interview prep", "coding interview", "bangla interview prep", "dsa practice", "system design"];

export function pageMetadata(title: string, description: string, route: string): Metadata {
  const canonical = `${SITE_URL}${route === "/" ? "/" : route.endsWith("/") ? route : `${route}/`}`;
  return {
    title,
    description,
    keywords: KEYWORDS,
    authors: [{ name: "RA Fahim", url: OWNER_URL }],
    creator: "RA Fahim",
    alternates: { canonical },
    openGraph: {
      type: "website",
      locale: "en_BD",
      url: canonical,
      siteName: SITE_NAME,
      title: `${title} | InterviewPrep BD by RA Fahim`,
      description,
      images: [{ url: `${SITE_URL}/og-image.svg`, width: 1200, height: 630, alt: "InterviewPrep BD by RA Fahim" }]
    },
    twitter: {
      card: "summary_large_image",
      creator: "@rafahimn",
      title: `${title} | InterviewPrep BD by RA Fahim`,
      description,
      images: [`${SITE_URL}/og-image.svg`]
    }
  };
}
