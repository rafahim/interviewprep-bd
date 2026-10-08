import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const base = "https://rafahim.com/interview-prep";
const contentRoot = path.join(process.cwd(), "content");
const staticRoutes = ["/", "/questions/", "/practice/", "/progress/", "/flashcards/"];

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true }).catch(() => []);
  const files = [];
  for (const entry of entries) {
    const full = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await walk(full));
    else if (entry.isFile() && entry.name.endsWith(".mdx")) files.push(full);
  }
  return files;
}

const files = await walk(contentRoot);
const slugs = [];
for (const file of files) {
  const source = await readFile(file, "utf8");
  const match = source.match(/^\s*"slug"\s*:\s*"([^"]+)"/m) || source.match(/^slug:\s*([^\n]+)$/m);
  if (match) slugs.push(match[1].trim().replace(/^['"]|['"]$/g, ""));
}
const routes = [...staticRoutes, ...slugs.map((slug) => `/questions/${slug}/`)];
const body = routes.map((route) => `  <url><loc>${base}${route}</loc><changefreq>${route.startsWith("/questions/") ? "monthly" : "weekly"}</changefreq><priority>${route === "/" ? "1.0" : route.startsWith("/questions/") ? "0.7" : "0.8"}</priority></url>`).join("\n");
const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`;
await writeFile(path.join(process.cwd(), "public", "sitemap.xml"), xml, "utf8");
console.log(`Wrote sitemap with ${routes.length} URLs.`);
