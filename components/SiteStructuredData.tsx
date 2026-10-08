import { SITE_URL, DEFAULT_DESCRIPTION } from "@/lib/seo";

export function SiteStructuredData() {
  const schema = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Person",
        "name": "RA Fahim",
        "url": "https://rafahim.com",
        "jobTitle": "Web Developer & Creator",
        "description": "Full-stack web developer with 1 year of experience, based in Dhaka, Bangladesh.",
        "address": { "@type": "PostalAddress", "addressLocality": "Dhaka", "addressCountry": "BD" },
        "sameAs": ["https://github.com/rafahim", "https://twitter.com/rafahimn", "https://linkedin.com/in/rafahimn"]
      },
      {
        "@type": "WebSite",
        "name": "InterviewPrep BD",
        "url": `${SITE_URL}/`,
        "description": DEFAULT_DESCRIPTION,
        "inLanguage": ["bn", "en"],
        "publisher": { "@type": "Person", "name": "RA Fahim", "url": "https://rafahim.com" }
      }
    ]
  };
  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />;
}
