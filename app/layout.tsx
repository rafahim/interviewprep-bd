import type { Metadata, Viewport } from "next";
import "./globals.css";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { SiteStructuredData } from "@/components/SiteStructuredData";
import { SITE_URL, DEFAULT_DESCRIPTION, KEYWORDS } from "@/lib/seo";

export const metadata: Metadata = {
  metadataBase: new URL("https://rafahim.com"),
  title: { default: "InterviewPrep BD by RA Fahim", template: "%s | InterviewPrep BD by RA Fahim" },
  description: DEFAULT_DESCRIPTION,
  keywords: KEYWORDS,
  authors: [{ name: "RA Fahim", url: "https://rafahim.com" }],
  creator: "RA Fahim",
  alternates: { canonical: `${SITE_URL}/` },
  openGraph: {
    type: "website",
    locale: "en_BD",
    url: `${SITE_URL}/`,
    siteName: "InterviewPrep BD",
    title: "InterviewPrep BD by RA Fahim",
    description: DEFAULT_DESCRIPTION,
    images: [{ url: `${SITE_URL}/og-image.svg`, width: 1200, height: 630, alt: "InterviewPrep BD by RA Fahim" }]
  },
  twitter: {
    card: "summary_large_image",
    creator: "@rafahimn",
    title: "InterviewPrep BD by RA Fahim",
    description: DEFAULT_DESCRIPTION,
    images: [`${SITE_URL}/og-image.svg`]
  },
  manifest: "/interview-prep/manifest.json",
  icons: { icon: "/interview-prep/favicon.svg", shortcut: "/interview-prep/favicon.svg" }
};

export const viewport: Viewport = {
  themeColor: "#070a12",
  colorScheme: "dark",
  width: "device-width",
  initialScale: 1
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="bn" className="dark">
      <body className="font-sans antialiased">
        <SiteStructuredData />
        <Navbar />
        <main className="min-h-[calc(100vh-160px)]">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
