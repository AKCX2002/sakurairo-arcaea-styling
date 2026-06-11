import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const SITE = "https://babel36acl.xyz";
const posts = JSON.parse(await readFile(path.resolve("src/data/posts.json"), "utf8"));
const pages = JSON.parse(await readFile(path.resolve("src/data/pages.json"), "utf8"));
const routes = ["", ...posts.map((post) => post.route), ...pages.map((page) => page.route)];

function loc(route) {
  const segments = route
    .split("/")
    .filter(Boolean)
    .map((segment) => encodeURIComponent(segment));
  return `${SITE}/${segments.join("/")}${segments.length > 0 ? "/" : ""}`;
}

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${routes.map((route) => `  <url><loc>${loc(route)}</loc></url>`).join("\n")}
</urlset>
`;

await mkdir(path.resolve("dist"), { recursive: true });
await writeFile(path.resolve("dist/sitemap.xml"), xml);
console.log(`Generated sitemap.xml with ${routes.length} URLs.`);
